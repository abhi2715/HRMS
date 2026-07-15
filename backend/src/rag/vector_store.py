"""
Vector Store — Qdrant integration for document embeddings and semantic search.

This module manages:
  - Connection to Qdrant vector database
  - Collection creation and management
  - Document chunking and embedding
  - Semantic similarity search
"""

from __future__ import annotations

import hashlib
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


# ── Configuration ────────────────────────────────────────────

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "hr_policies"
EMBEDDING_DIM = 384  # Sentence-transformers 'all-MiniLM-L6-v2' dimension


# ── Document Chunker ─────────────────────────────────────────

class DocumentChunker:
    """Splits documents into overlapping chunks for embedding."""

    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, metadata: dict | None = None) -> list[dict]:
        """Split text into chunks with metadata."""
        words = text.split()
        chunks = []
        step = self.chunk_size - self.overlap

        for i in range(0, len(words), step):
            chunk_words = words[i : i + self.chunk_size]
            if len(chunk_words) < 20:  # Skip very small trailing chunks
                continue

            chunk_text = " ".join(chunk_words)
            chunk_id = hashlib.md5(chunk_text[:100].encode()).hexdigest()

            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    **(metadata or {}),
                    "chunk_index": len(chunks),
                    "word_count": len(chunk_words),
                },
            })

        return chunks


# ── Simple Embedding (CPU-friendly) ─────────────────────────

class SimpleEmbedder:
    """Lightweight embedding using bag-of-words TF hashing.

    In production, replace with:
      - sentence-transformers ('all-MiniLM-L6-v2')
      - OpenAI Embeddings API
      - Google Vertex AI text-embedding
    """

    def __init__(self, dim: int = EMBEDDING_DIM):
        self.dim = dim

    def embed(self, text: str) -> list[float]:
        """Generate a deterministic pseudo-embedding via feature hashing."""
        import struct

        vector = [0.0] * self.dim
        words = text.lower().split()

        for word in words:
            h = int(hashlib.sha256(word.encode()).hexdigest(), 16)
            idx = h % self.dim
            sign = 1.0 if (h // self.dim) % 2 == 0 else -1.0
            vector[idx] += sign

        # L2 normalize
        magnitude = sum(v * v for v in vector) ** 0.5
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(t) for t in texts]


# ── Vector Store Client ──────────────────────────────────────

class VectorStore:
    """Qdrant-compatible vector store with fallback in-memory mode.

    When Qdrant is unavailable, falls back to a simple in-memory
    cosine similarity search for development/demo purposes.
    """

    def __init__(self):
        self.embedder = SimpleEmbedder()
        self.chunker = DocumentChunker()
        self._qdrant_client = None
        self._memory_store: list[dict] = []  # Fallback in-memory
        self._connected = False
        self._try_connect()

    def _try_connect(self):
        """Attempt to connect to Qdrant. Falls back to in-memory if unavailable."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            if QDRANT_URL and QDRANT_API_KEY:
                self._qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=10)
            else:
                self._qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, timeout=5)
            # Ensure collection exists
            collections = [c.name for c in self._qdrant_client.get_collections().collections]
            if COLLECTION_NAME not in collections:
                self._qdrant_client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")
            self._connected = True
            logger.info(f"Connected to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        except Exception as e:
            logger.warning(f"Qdrant unavailable ({e}), using in-memory fallback")
            self._connected = False

    async def add_document(self, text: str, metadata: dict | None = None) -> int:
        """Chunk and store a document. Returns number of chunks stored."""
        chunks = self.chunker.chunk(text, metadata)

        if self._connected and self._qdrant_client:
            from qdrant_client.models import PointStruct

            points = []
            for i, chunk in enumerate(chunks):
                vector = self.embedder.embed(chunk["text"])
                points.append(PointStruct(
                    id=abs(hash(chunk["id"])) % (2**63),
                    vector=vector,
                    payload={"text": chunk["text"], **chunk["metadata"]},
                ))

            self._qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
        else:
            # In-memory fallback
            for chunk in chunks:
                self._memory_store.append({
                    "text": chunk["text"],
                    "vector": self.embedder.embed(chunk["text"]),
                    "metadata": chunk["metadata"],
                })

        logger.info(f"Stored {len(chunks)} chunks (connected={self._connected})")
        return len(chunks)

    async def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Semantic search for the most relevant document chunks."""
        query_vector = self.embedder.embed(query)

        if self._connected and self._qdrant_client:
            results = self._qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vector,
                limit=top_k,
            )
            return [
                {"text": r.payload.get("text", ""), "score": r.score, "metadata": r.payload}
                for r in results
            ]
        else:
            # In-memory cosine similarity search
            scores = []
            for item in self._memory_store:
                dot = sum(a * b for a, b in zip(query_vector, item["vector"]))
                scores.append((dot, item))

            scores.sort(key=lambda x: x[0], reverse=True)
            return [
                {"text": s[1]["text"], "score": s[0], "metadata": s[1]["metadata"]}
                for s in scores[:top_k]
            ]

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def document_count(self) -> int:
        if self._connected and self._qdrant_client:
            info = self._qdrant_client.get_collection(COLLECTION_NAME)
            return info.points_count
        return len(self._memory_store)


# ── Singleton ────────────────────────────────────────────────
vector_store = VectorStore()
