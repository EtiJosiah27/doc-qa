from __future__ import annotations

import chromadb
from chromadb.api.models.Collection import Collection

def get_chroma_collection(name: str = "docs") -> Collection:
    client = chromadb.PersistentClient("./data/chroma")
    return client.get_or_create_collection(name=name)