from __future__ import annotations
from pydantic import BaseModel
from typing import List

class DocumentPage(BaseModel):
    page_num: int
    text: str

class DocumentText(BaseModel):
    doc_id: str
    source_path: str
    pages: List[DocumentPage]
