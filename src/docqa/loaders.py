from __future__ import annotations

from pathlib import Path
from pypdf import PdfReader
import hashlib

from docx import Document as DocxDocument

from docqa.models import DocumentText, DocumentPage

def make_doc_id_from_file(path: Path) -> str:
    """
    doc_id: filename + short hash of file contents.
    This avoids collisions when different files have the sane name.
    """
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()[:12]
    return f"{path.stem}-{digest}"

def check_file_path(path: str):
    p = path
    ext = ".txt"

    extension = p.suffix.lower()

    if extension == ".txt":
        ext = ".txt"

    if extension == ".docx":
        ext = ".docx"

    if extension == ".pdf":
        ext = ".pdf"

    if not p.exists():
        raise FileNotFoundError(f"{ext} file not found: {p}")

def load_text(path: str) -> DocumentText:
    p = Path(path)

    check_file_path(p)
    
    text = p.read_text(encoding="utf-8", errors="replace")

    return DocumentText(
        doc_id=make_doc_id_from_file(p),
        source_path=str(p),
        pages=[DocumentPage(page_num=1, text=text)],
    )

def load_docx(path: str) -> DocumentText:
    p = Path(path)
    
    check_file_path(p)

    docx = DocxDocument(str(p))

    paragraphs = []
    for para in docx.paragraphs:
        t = para.text.strip()
        if t:
            paragraphs.append(t)

    text = "\n".join(paragraphs)

    return DocumentText(
        doc_id=make_doc_id_from_file(p),
        source_path=str(p),
        pages=[DocumentPage(page_num=1, text=text)]
    )

def load_pdf(path: str) -> DocumentText:
    p = Path(path)

    check_file_path(p)

    reader = PdfReader(str(p))

    pages: list[DocumentPage] = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(DocumentPage(page_num=i, text=text))

    return DocumentText(
        doc_id = make_doc_id_from_file(p),
        source_path = str(p),
        pages = pages,
    )

def load_document(path: str) -> DocumentText:
    p = Path(path)

    ext = p.suffix.lower()

    if ext == ".txt":
        return load_text(path)
    
    if ext == ".docx":
        return load_docx(path)
    
    if ext == ".pdf":
        return load_pdf(path)
    
    raise ValueError(f"Unsupported file type: {ext}")

