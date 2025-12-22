import argparse


def cmd_ingest(args: argparse.Namespace) -> int:
    print(f"[stub] ingest path={args.path} collection={args.collection}")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    print(f"[stub] ask question={args.question!r} collection={args.collection}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m app", description="Local Document Q&A (RAG) CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Ingest a document into the vector store")
    ingest.add_argument("path", help="Path to a TXT, PDF, or DOCX file")
    ingest.add_argument("--collection", default="docs", help='Chroma collection name (default: "docs")')
    ingest.set_defaults(func=cmd_ingest)

    ask = sub.add_parser("ask", help="Ask a question against ingested documents")
    ask.add_argument("question", help="Question in quotes")
    ask.add_argument("--collection", default="docs", help='Chroma collection name (default: "docs")')
    ask.set_defaults(func=cmd_ask)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
