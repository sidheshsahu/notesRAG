# notesRAG

`notesRAG` is an in-progress audio question-answering project built around a simple RAG flow:

1. Upload an audio file in the Streamlit UI
2. Transcribe it with AssemblyAI
3. Split the transcript into chunks
4. Store embeddings in Pinecone
5. Retrieve relevant transcript chunks
6. Generate an answer with Groq

This repository is currently being built iteratively, so this README describes the project as it exists today.

## Current Status

What is working right now:

- Streamlit UI for uploading audio and asking a question
- Audio transcription through AssemblyAI
- Transcript chunking with LangChain
- Embedding generation with Google Generative AI embeddings
- Vector storage and retrieval with Pinecone
- Final answer generation with Groq

## Project Flow

The current application flow is:

`Streamlit upload -> temporary file -> AssemblyAI transcription -> transcript chunking -> Pinecone vector store -> retrieval -> Groq answer`

Main implementation files:

- `app.py` - Streamlit entrypoint
- `pipeline/workflow.py` - end-to-end RAG pipeline
- `data/audio_text.py` - audio upload + transcription polling logic
- `pipeline/document_store.py` - Pinecone index creation
- `pipeline/llm_call.py` - LLM configuration
- `pipeline/prompt.py` - answer prompt template

## Tech Stack

- Python 3.11+
- Streamlit
- LangChain
- AssemblyAI
- Pinecone
- Groq

## Setup

### 1. Clone the repo

```powershell
git clone <your-repo-url>
cd notesRAG
```

### 2. Create and activate a virtual environment

If you use `uv`:

```powershell
uv sync
```

If you prefer standard `venv` + `pip`, install dependencies from `pyproject.toml` manually.

### 3. Add environment variables

Create a `.env` file in the project root with the keys used by the current code:

```env
ASSEMBLYAI_API_KEY=your_assemblyai_key
PINECONE_API_KEY=your_pinecone_key
GROQ_API_KEY=your_groq_key

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=audio_texts_rag
```

Notes:

- `ASSEMBLYAI_API_KEY` is used for transcription
- `PINECONE_API_KEY` is used to create/access the vector index
- `GROQ_API_KEY` is used for final answer generation
- LangSmith variables are optional for tracing, but included in the current setup

## Running the App

Start the Streamlit app:

```powershell
streamlit run app.py
```

Then:

1. Upload an audio file
2. Enter a question about the audio
3. Wait for transcription, indexing, retrieval, and answer generation

Supported upload types in the UI:

- `mp3`
- `wav`
- `m4a`
- `mp4`
- `mpeg`
- `mpga`

