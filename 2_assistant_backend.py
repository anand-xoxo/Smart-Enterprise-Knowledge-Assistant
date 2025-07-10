# assistant_backend.py
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import fitz  # PyMuPDF
import tiktoken
import weaviate
from weaviate.classes.init import Auth
from openai import OpenAI
from dotenv import load_dotenv
import redis
import json
from weaviate.classes.config import Property, Configure, DataType

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

# OpenAI Client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Weaviate Client
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers={"X-OpenAI-Api-Key": OPENAI_API_KEY}
)

# Redis Client
import redis

UPSTASH_URL = "rediss://default:Ad7NAAIjcDE5ZWZiNzY2MWQzMzQ0NTEwYTk5MjlhYzMwNGZiMTkxMXAxMA@rational-ferret-57037.upstash.io:6379" #change this to your own upstash_url 

r = redis.from_url(UPSTASH_URL, decode_responses=True)

# Create collection (if not exists)
from weaviate.classes.config import Property, Configure, DataType

def create_collection(topic):
    name = topic.lower().replace(" ", "_")  # Normalize
    existing = [c.lower() for c in client.collections.list_all()]
    
    if name not in existing:
        client.collections.create(
            name=name,
            properties=[
                Property(name="chunk_id", data_type=DataType.TEXT, description="Chunk identifier"),
                Property(name="content", data_type=DataType.TEXT, description="Chunk content")
            ],
            vectorizer_config=Configure.Vectorizer.text2vec_openai()
        )
        print(f"✅ Created collection: {name}")
    else:
        print("✅ Collection already exists")
    return name


# PDF extraction and chunking
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text("text") for page in doc)

def chunk_text(text, max_tokens=800):
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    return [encoder.decode(tokens[i:i + max_tokens]) for i in range(0, len(tokens), max_tokens)]

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai_client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

# Store in Weaviate
def add_pdf_to_collection(pdf_path, topic):
    collection_name = create_collection(topic)  # Creates or skips
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    collection = client.collections.get(collection_name)
    
    for idx, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.data.insert(
            properties={
                "chunk_id": f"{topic}_{idx}",
                "content": chunk
            },
            vector=embedding
        )
    
    print(f"✅ Uploaded {len(chunks)} chunks to collection: '{collection_name}'")
    return len(chunks)

# Semantic search
def search_docs(query, collection_name, top_k=5):
    embedding = get_embedding(query)
    collection = client.collections.get(collection_name)
    results = collection.query.near_vector(embedding, limit=top_k)
    return results.objects


# Redis Memory
def get_chat_memory(user_id, topic):
    key = f"chat:{user_id}:{topic}"
    data = r.get(key)
    return json.loads(data) if data else []

def save_chat_memory(user_id, topic, memory):
    key = f"chat:{user_id}:{topic}"
    r.set(key, json.dumps(memory))

# Generate response
def generate_answer(query, user_id, topic):
    # Each topic is now its own collection
    collection_name = topic.lower().replace(" ", "_")
    
    # Search directly in the topic-specific collection
    results = search_docs(query, collection_name=collection_name)
    if not results:
        return "No relevant content found."

    context = "\n\n".join(r.properties["content"] for r in results)

    # Retrieve conversation history
    chat_memory = get_chat_memory(user_id, topic)
    chat_memory.append({"role": "user", "content": query})

    # Format the messages for GPT
    messages = [
        {"role": "system", "content": "You are an internal knowledge assistant. Answer using only the given context."},
        {"role": "system", "content": f"Context:\n{context}"}
    ] + chat_memory

    # Generate response from OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    answer = response.choices[0].message.content
    chat_memory.append({"role": "assistant", "content": answer})

    # Save conversation back to memory
    save_chat_memory(user_id, topic, chat_memory)

    return answer

# ... all your assistant functions above ...

# Safely close Weaviate connection on exit
import atexit
atexit.register(client.close)
