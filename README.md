# 📄 DocQA Chatbot

An interactive Streamlit-powered chatbot that answers questions from uploaded documents using local language models and vector embeddings. It supports PDF, DOCX, and TXT files.

## 🚀 Features

- 📁 Upload and parse PDF, DOCX, or TXT files.
- ✂️ Split large documents into smaller, searchable chunks.
- 🔍 Embed content using HuggingFace models and store it in Chroma vector DB.
- 💬 Ask questions and get relevant answers along with source references.
- 🧠 Powered by LangChain, HuggingFace, and Sentence-Transformers.

## 🛠️ Stack

- Python 3.11+
- Streamlit
- LangChain
- Sentence-Transformers
- HuggingFace Embeddings
- Chroma DB
- PyPDF / docx2txt

## 🧪 Example Usage
Upload a .pdf, .docx, or .txt file using the uploader. Then ask a question like:

What are the key findings in the document?

Summarize the second section.

Who is the author or target audience?

The app will process the document, chunk it, embed it using all-MiniLM-L6-v2, store embeddings in Chroma, and return answers using a local question-answering chain.

## 📌 Notes
This chatbot uses a small but powerful model (all-MiniLM-L6-v2) to allow fast, offline use without needing a GPU or large downloads. Ideal for low-resource environments or quick prototypes. For future upgrades, you can replace the embedding model or chain logic with more advanced components. If you're getting LangChain deprecation warnings, upgrade to the latest imports (e.g., langchain-huggingface, langchain-community). No internet is required for basic QA after models are cached. Keep your uploaded files in the data/uploads folder.

## 📦 Setup Instructions

```bash
git clone https://github.com/your-username/docqa-chatbot.git
cd docqa-chatbot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py

Then open http://localhost:8501 in your browser.


📂 Project Structure

docqa-chatbot/
├── app/
│   ├── ingest.py
│   └── qa_engine.py
├── interface/
│   └── streamlit_app.py
├── main.py
├── data/
│   └── uploads/
├── requirements.txt
└── README.md