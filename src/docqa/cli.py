from __future__ import annotations

import argparse

from docqa.loaders import load_document
from docqa.chunking import chunk_document
from docqa.store import store_records_in_chroma
from docqa.vectorstore import get_chroma_collection
from docqa.retrieval import search, print_results

def ingest_cmd(path: str, chunk_size: int, overlap: int) -> None:
    doc = load_document(path)
    records = chunk_document(doc, chunk_size=chunk_size, overlap=overlap)
    stored = store_records_in_chroma(records, collection_name="docs")

    print("INGEST RESULT")
    print(f"doc_id: {doc.doc_id}")
    print(f"pages: {len(doc.pages)}")
    print(f"chunks: {len(records)}")
    print(f"stored: {stored} chunks")

    col = get_chroma_collection("docs")
    items = col.get(limit=5)
    print(items["ids"])
    print(items["metadatas"])

def ask_cmd(question: str, top_k: int, doc_id: str | None) -> None:
    results = search(question, top_k=top_k, doc_id=doc_id, collection_name="docs")
    print_results(results, snipper_len=300)

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest")
    ingest.add_argument("path")
    ingest.add_argument("--chunk-size", type=int, default=1000)
    ingest.add_argument("--overlap", type=int, default=200)

    ask = sub.add_parser("ask")
    ask.add_argument("question")
    ask.add_argument("--top-k", type=int, default=5)
    ask.add_argument("--doc_id", default=None)

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_cmd(args.path, chunk_size=args.chunk_size, overlap=args.overlap)

    if args.command == "ask":
        ask_cmd(args.question, args.top_k, args.doc_id)

if __name__ == "__main__":
        main()