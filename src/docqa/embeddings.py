from __future__ import annotations

import os
from typing import List

from openai import OpenAI

def embed_texts(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    
    client = OpenAI()
    resp = client.embeddings.create(model=model, input=texts)

    return [item.embedding for item in resp.data]