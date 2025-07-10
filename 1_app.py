# app.py

import streamlit as st
from assistant_backend import add_pdf_to_collection, generate_answer, create_collection

st.set_page_config(page_title="EnterpriSense Assistant", layout="wide")

st.title("📚 EnterpriSense: Enterprise Knowledge Assistant")

tab1, tab2 = st.tabs(["📁 Upload PDF", "💬 Ask a Question"])



with tab1:
    st.header("Upload Internal Document")
    pdf = st.file_uploader("Upload a PDF", type=["pdf"])
    topic = st.text_input("Enter topic name (e.g. HR_Manual)")

    if st.button("Upload and Process PDF"):
        if pdf and topic:
            with open("temp.pdf", "wb") as f:
                f.write(pdf.read())
            count = add_pdf_to_collection("temp.pdf", topic) 
            st.success(f"✅ Uploaded and processed {count} chunks under topic '{topic}'")
        else:
            st.warning("Please upload a PDF and enter a topic name.")


with tab2:
    st.header("Chat with the Assistant")
    user_id = st.text_input("Enter your Employee ID", value="emp001")
    chat_topic = st.text_input("Enter topic (e.g. HR_Manual)", value="HR_Manual")
    query = st.text_input("Ask a question")

    if st.button("Submit"):
        if query and user_id and chat_topic:
            answer = generate_answer(query, user_id, chat_topic) 
            st.markdown(f"**🧠 Assistant:** {answer}")
        else:
            st.warning("Please enter all required fields.")

