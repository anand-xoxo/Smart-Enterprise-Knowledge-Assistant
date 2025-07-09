# Smart-Enterprise-Knowledge-Assistant
AI-powered assistant for enterprise policy and HR knowledge systems

It uses **Retrieval-Augmented Generation (RAG)** powered by **OpenAI GPT-4o** and **Weaviate** vector database, all wrapped in an intuitive **Streamlit UI**.

---

## 🚀 Key Features

- 📁 **Upload Documents**: Upload PDFs like policy manuals or onboarding guides.
- 🧠 **Smart Chunking & Embedding**: Uses `tiktoken` and OpenAI embeddings for context-aware chunking.
- 🔍 **Semantic Search**: Uses Weaviate for fast and relevant vector-based retrieval.
- 💬 **Conversational Q&A**: Ask questions and receive accurate answers from GPT-4o using only document context.
- 🧠 **Chat Memory**: Keeps conversation flow using session-based memory.
- 🎯 **Topic Filtering**: Query specific sets of documents by topic name.

---

## 🖥️ UI Preview

--still in work--

---

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python, OpenAI, PyMuPDF, tiktoken
- **Vector DB**: [Weaviate Cloud](https://weaviate.io/)
- **LLM**: OpenAI GPT-4o (`text-embedding-ada-002` for embeddings)

---

## 📁 Project Structure

