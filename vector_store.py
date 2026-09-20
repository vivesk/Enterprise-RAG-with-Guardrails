import chromadb
from sentence_transformers import SentenceTransformer

from .chunking import TextChunk
from .config import settings


class VectorStore:
    """Small abstraction around Chroma + Sentence Transformers.

    The abstraction makes it easier to replace Chroma with Azure AI Search
    or another managed vector service later.
    """

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection(
            name="enterprise_rag"
        )
        self.encoder = SentenceTransformer(settings.embedding_model)

    def add_chunks(self, chunks: list[TextChunk]) -> int:
        """Embed and persist document chunks."""
        if not chunks:
            return 0

        documents = [c.text for c in chunks]
        self.collection.upsert(
            ids=[c.chunk_id for c in chunks],
            documents=documents,
            metadatas=[{"source": c.source} for c in chunks],
            embeddings=self.encoder.encode(
                documents, normalize_embeddings=True
            ).tolist(),
        )
        return len(chunks)

    def search(self, query: str, top_k: int) -> list[dict]:
        """Return the top semantic matches for a query."""
        embedding = self.encoder.encode(
            [query], normalize_embeddings=True
        )[0].tolist()

        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        return [
            {
                "text": result["documents"][0][i],
                "source": result["metadatas"][0][i]["source"],
                "chunk_id": result["ids"][0][i],
                "distance": result["distances"][0][i],
            }
            for i in range(len(result["documents"][0]))
        ]
