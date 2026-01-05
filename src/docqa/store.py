from __future__ import annotations

from typing import Dict, Any, List

from docqa.vectorstore import get_chroma_collection
from docqa.embeddings import embed_texts

def make_chunk_ids(records: List[Dict[str, Any]]) -> List[str]:
    return [f"{r['doc_id']}:{r['page']}:{r['chunk_id']}" for r in records]

def store_records_in_chroma(records: List[Dict[str, Any]], collection_name: str = "docs") -> int:
    if not records: return 0

    collection = get_chroma_collection(collection_name)

    ids = make_chunk_ids(records)
    docs = [r["text"] for r in records]
    metadatas = [
        {
            "doc_id": r["doc_id"],
            "page" : r["page"],
            "chunk_id" : r["chunk_id"],
            "source_path" : r["source_path"],
        }
        for r in records
    ]

    embeddings = embed_texts(docs)

    collection.upsert(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return len(records)
