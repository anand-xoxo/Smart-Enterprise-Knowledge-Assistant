# Smart-Enterprise-Knowledge-Assistant
AI-powered assistant for enterprise policy and HR knowledge systems

It uses **Retrieval-Augmented Generation (RAG)** powered by **OpenAI GPT-4o** and **Weaviate** vector database, all wrapped in an intuitive **Streamlit UI**.

---

## 🚀 Key Features

- 📁 **PDF Upload**: Upload any internal policy or guideline PDF to create a searchable knowledge base.
- 🧠 **Retrieval-Augmented Generation (RAG)**: Combines OpenAI embeddings and GPT-4o to give grounded, context-aware answers.
- 🗂️ **One Collection per Topic**: Each document topic (e.g., HR, IT, Security) is stored in its own Weaviate collection.
- 💬 **Chat with Memory**: Stores user-specific chat history using Redis.
- 🌐 **Interactive Streamlit UI**: Upload files and interact with the assistant through a friendly web interface.
- ⚡ Fast responses with vector-based semantic search.
---

## 🖥️ UI Preview
Uploading a document:-

![Screenshot 2025-07-10 143330](https://github.com/user-attachments/assets/2c7f9941-34e3-4ba1-a6b4-dd035ffc4c4b)


Raising a query:-

![Screenshot 2025-07-10 143526](https://github.com/user-attachments/assets/b924e3e8-f396-4564-abcc-bab2a6cb68d9)


## 🛠️ Tech Stack

| Tool         | Purpose                                |
|--------------|----------------------------------------|
| `OpenAI GPT-4o` | Generates answers using chat context |
| `text-embedding-ada-002` | Embeds document chunks semantically |
| `Weaviate`    | Stores vectorized content for search  |
| `Redis`       | Stores user-wise conversational memory |
| `Streamlit`   | Web-based UI for uploading & chatting |
| `PyMuPDF`     | Extracts text from PDFs               |
| `tiktoken`    | Token-based chunking of documents     |

---



## 📁 Project Structure
1). app.py                      # Streamlit UI

2). assistant_backend.py       # Core RAG logic

3). .env (write your api keys here and other secured details in this env file)

4). README.md

