from __future__ import annotations

from typing import Any, Dict, List, Optional

from docqa.vectorstore import get_chroma_collection
from docqa.embeddings import embed_texts

def search(query: str, top_k: int = 5, doc_id: Optional[str] = None, collection_name: str = "docs") -> List[Dict[str, Any]]:
    if query.strip() == "":
        return[]
    
    colletion = get_chroma_collection(collection_name)

    query_embedding = embed_texts([query])[0]

    where = {"doc_id" : doc_id} if doc_id else None

    res = colletion.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    results: List[Dict[str,Any]] = []
    for text, meta, dist in zip(docs, metas, dists):
        results.append({
            "distance": dist,
            "doc_id": meta.get("doc_id"),
            "page" : meta.get("page"),
            "chunk_id": meta.get("chunk_id"),
            "source_path": meta.get("source_path"),
            "text": text
        })

    return results

def print_results(results: List[Dict[str, Any]], snipper_len = 300) -> None:
    if not results:
        print("No results found.")
        return
    
    for i, r in enumerate(results, start=1):
        text = (r["text"] or "").strip()
        snippet = text[:snipper_len].replace("\n", " ")
        print(f"\n#{i}  distance={r['distance']:.4f}")
        print(f"    doc_id={r['doc_id']}    page={r['page']}    chunk_id={r['chunk_id']}")
        print(f"    source={r['source_path']}")
        print(f"    snippet:{snippet}...")