from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def llm():
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
    return llm
