from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH, COLLECTION_NAME, TOP_K

DATA_DIR = Path("data")

class RAGEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        if self.collection.count() == 0:
            self.ingest_files()

    def chunk_text(self, text, chunk_size=800, overlap=100):
        chunks = []
        start = 0
        while start < len(text):
            chunks.append(text[start:start + chunk_size])
            start += chunk_size - overlap
        return chunks

    def ingest_files(self):
        documents, metadatas = [], []
        for path in DATA_DIR.glob("*.txt"):
            chunks = self.chunk_text(path.read_text(encoding="utf-8"))
            documents.extend(chunks)
            metadatas.extend([{"source": path.name} for _ in chunks])

        if not documents:
            return

        embeddings = self.embedding_model.encode(documents).tolist()
        ids = [f"doc_{i}" for i in range(len(documents))]
        self.collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    def search(self, query):
        count = self.collection.count()
        if count == 0:
            return [], []
        query_embedding = self.embedding_model.encode([query]).tolist()
        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(TOP_K, count),
        )
        return result["documents"][0], result["metadatas"][0]
