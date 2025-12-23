from __future__ import annotations

import argparse

from docqa.loaders import load_document

def ingest_cmd(path: str) -> None:
    doc = load_document(path)
    page_count = len(doc.pages)
    non_empty_pages = sum(1 for p in doc.pages if p.text.strip() != "")
    total_chars = sum(len(p.text) for p in doc.pages)

    preview = doc.pages[0].text[:200].replace("\n", "\\n")

    print("INGEST RESULT")
    print(f"doc_id: {doc.doc_id}")
    print(f"pages: {page_count}")
    print(f"non_empty_pages: {non_empty_pages}")
    print(f"character_count: {total_chars}")
    # print(f"preview: {preview}")

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("path")
    args = parser.parse_args()
    if args.command == "ingest":
        ingest_cmd(args.path)

if __name__ == "__main__":
        main()