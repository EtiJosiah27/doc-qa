# doc-qa

Local document Q&A (RAG) project.

## Setup
python3 -m venv .venv
source .venv/bin/activate
pip install chromadb pydantic python-docx pypdf tiktoken openai

## Run
python -m app ingest sample.txt
python -m app ask "test question"
