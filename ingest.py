from rag import RAGEngine

if __name__ == "__main__":
    rag = RAGEngine()
    print(f"RAG database contains {rag.collection.count()} chunks.")
