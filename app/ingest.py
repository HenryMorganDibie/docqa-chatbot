# app/ingest.py

import os
import shutil
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings
from config.settings import CHROMA_DB_DIR


def load_document(file_path):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    return loader.load()


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)


def deduplicate_chunks(chunks):
    """Remove duplicate chunks based on their text content."""
    unique = {chunk.page_content: chunk for chunk in chunks}
    return list(unique.values())


def embed_and_store(docs):
    print(f"📄 Loaded {len(docs)} raw docs.")

    chunks = split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks.")

    chunks = deduplicate_chunks(chunks)
    print(f"🧹 Deduplicated to {len(chunks)} unique chunks.")

    # Remove previous Chroma DB
    try:
        if os.path.exists(CHROMA_DB_DIR):
            shutil.rmtree(CHROMA_DB_DIR)
            print(f"🗑️ Deleted old Chroma DB at {CHROMA_DB_DIR}")
    except PermissionError:
        print("⚠️ Could not delete the Chroma DB. Make sure no other process is using it.")

    # ✅ Remove model_kwargs
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

    vectordb.persist()
    print(f"✅ New Chroma DB created at {CHROMA_DB_DIR}")
    return vectordb
