from langchain_core.prompts import PromptTemplate


def template():
    rag_prompt = PromptTemplate.from_template(
        template="""You are a helpful assistant.
    Use only the provided context to answer the question.
    If the answer is not present in the context, say: "I don't know based on the provided context."

    Context:
    {context}

    Question:
    {question}

    Answer:"""
    )

    return rag_prompt
