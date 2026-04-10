import os
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import ServerlessSpec, Pinecone
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from pipeline.document_store import create_index
from pipeline.prompt import template
from pipeline.llm_call import llm
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from data.audio_text import transcribe_audio
from langchain_classic.schema import Document

load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def rag_pipeline(query, file_path):
    transcript = transcribe_audio(file_path)
    doc = Document(page_content=transcript, metadata={"source": "audio_file"})

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=5)
    texts = text_splitter.split_documents([doc])

    embedder = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview", output_dimensionality=384
    )

    vectorstore = PineconeVectorStore.from_documents(
        texts, embedder, index_name=create_index()
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    )

    rag_chain = RunnableParallel(
        {
            "question": RunnablePassthrough(),
            "context": retriever | RunnableLambda(format_docs),
        }
    )

    parser = StrOutputParser()
    output = rag_chain | template() | llm() | parser
    result = output.invoke(query)
    return result
