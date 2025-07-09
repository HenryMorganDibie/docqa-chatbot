# interface/streamlit_app.py
import streamlit as st
import os
from app.ingest import load_document, split_documents, embed_and_store
from app.qa_engine import build_qa_chain

def run_app():
    st.title("📄 Document Q&A Chatbot")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    question = st.text_input("Ask a question about the document")

    if uploaded_file:
        file_path = os.path.join("data", "uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        docs = load_document(file_path)
        chunks = split_documents(docs)
        docs = load_document(file_path)
        vectordb = embed_and_store(docs)

        qa_chain = build_qa_chain(vectordb)

        if question:
           response = qa_chain.invoke({"query": question})
           answer = response["result"]
           st.success(answer)

           with st.expander("Sources"):
              for doc in response["source_documents"]:
                  st.markdown(f"**Source:** {doc.metadata.get('source', 'N/A')}")
                  st.text(doc.page_content[:300])  
