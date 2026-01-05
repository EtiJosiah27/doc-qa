from __future__ import annotations

from typing import List, Dict, Any

from docqa.models import DocumentText

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    if chunk_size <= 0 :
        raise ValueError("chunk_size must be > 0")
    if overlap < 0 :
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")
    
    text = text or ""
    if text.strip() == "" : 
        return []
    
    step = chunk_size - overlap
    chunks: List[str] = []

    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end]
        chunks.append(chunk)

        if end == n:
            break

        start += step

    return chunks

def chunk_document(
    doc: DocumentText,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> List[Dict[str, Any]]:
    
    records: List[Dict[str, Any]] = []

    for page in doc.pages:
        chunks = chunk_text(page.text, chunk_size=chunk_size, overlap=overlap)

        for i, chunk in enumerate(chunks):
            records.append(
                {
                    "doc_id": doc.doc_id,
                    "source_path": doc.source_path,
                    "page": page.page_num,
                    "chunk_id": f"p{page.page_num}-c{i}",
                    "text": chunk,
                }
            )

    return records
            

