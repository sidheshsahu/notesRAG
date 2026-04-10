import pymupdf
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    text_content = ""
    for page in doc:
        text = page.get_text()
        text_content += text

    doc.close()
    return text_content


llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

prompt = PromptTemplate.from_template(
    template="""You are given messy syllabus text extracted from a PDF.

Your task:
1. Identify modules (like 1, 2, 3...) and Module names appear BEFORE their subtopics.
2. Identify subtopics (like 1.1, 2.3 etc.)
3. Clean broken words and spacing
4. Ignore irrelevant sections (books, exams, links)
5. Convert into structured JSON

Rules:
- id should be like 1.1, 2.3

Output ONLY JSON:
{{
  "course_code": "",
  "course_name": "",
  "syllabus_index": [
    {{
      "id": "",
      "topic": "",
      "module": ""
    }}
  ]
}}

Text:
{text}"""
)

text = extract_text_from_pdf(r"D:\notesRAG\notesRAG\EVM Syllabus.pdf")

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke(
    {
        "text": text,
    }
)

print(result)
