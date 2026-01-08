from src.rag import TeamKnowledgeBase


def main():
    kb = TeamKnowledgeBase()

    print("Loading knowledge base...")
    kb.load("knowledge_base")

    print("Processing documents...")
    kb.process()

    print("Indexing...")
    kb.index()

    print("\nKnowledge base ready. Ask a question (Ctrl+C or Ctrl+D to exit).\n")

    while True:
        try:
            question = input("> ").strip()

            if not question:
                continue

            result = kb.ask(question)

            print("\nAnswer:\n")
            print(result["answer"])

            print("\nSources:")
            for src in result["sources"]:
                print(f"- {src['file']} ({src['author']}, {src['topic']})")
            print("\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting knowledge base. Goodbye.")
            break


if __name__ == "__main__":
    main()
