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
        end = (start + chunk_size, n)
        chunk = text[start:end]
        chunks.append(chunk)

        if end == n:
            break

        start += start

    return chunks