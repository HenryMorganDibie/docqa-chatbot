from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.chains import RetrievalQA


def build_qa_chain(vectordb):
    retriever = vectordb.as_retriever()

    model_name = "google/flan-t5-small"  # ✅ Lightweight and local
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

    llm = HuggingFacePipeline(pipeline=pipe)

    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
