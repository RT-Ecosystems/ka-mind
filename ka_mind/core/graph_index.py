"""
KA-Mind GraphIndex — FAISS-based fast semantic search.
Optional dependency. Falls back to linear search if FAISS not installed.
"""
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class GraphIndex:
    """FAISS-powered index for fast vector similarity search."""

    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = None
        self.atom_ids = []  # Maps index position → atom_id
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatIP(dim)  # Inner Product (cosine similarity)

    def add(self, atom_id: str, vector) -> bool:
        """Add a single atom's vector to the index."""
        if not FAISS_AVAILABLE or self.index is None:
            return False
        v = np.array(vector, dtype=np.float32).reshape(1, -1)
        # Normalize for cosine similarity
        faiss.normalize_L2(v)
        self.index.add(v)
        self.atom_ids.append(atom_id)
        return True

    def add_batch(self, items: list) -> int:
        """Add multiple (atom_id, vector) pairs at once."""
        if not FAISS_AVAILABLE or self.index is None or not items:
            return 0
        vectors = []
        for atom_id, vec in items:
            v = np.array(vec, dtype=np.float32)
            vectors.append(v)
            self.atom_ids.append(atom_id)
        if vectors:
            mat = np.array(vectors, dtype=np.float32)
            faiss.normalize_L2(mat)
            self.index.add(mat)
        return len(vectors)

    def search(self, query_vector, top_k: int = 10) -> list:
        """Search for most similar atoms. Returns [(atom_id, score), ...]."""
        if not FAISS_AVAILABLE or self.index is None or self.index.ntotal == 0:
            return []
        q = np.array(query_vector, dtype=np.float32).reshape(1, -1)
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, min(top_k, self.index.ntotal))
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0 and idx < len(self.atom_ids):
                results.append((self.atom_ids[idx], float(score)))
        return results

    @property
    def size(self) -> int:
        return self.index.ntotal if self.index else 0

    def is_available(self) -> bool:
        return FAISS_AVAILABLE and self.index is not None
