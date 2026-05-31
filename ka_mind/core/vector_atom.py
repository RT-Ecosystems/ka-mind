# KA-Mind Vector Atom — Semantic embedding
# BUG FIXED: Model now loads LAZILY (not at import time!)
import hashlib


class VectorAtom:
    _encoder = None  # Shared lazy-loaded model

    @classmethod
    def _get_encoder(cls):
        if cls._encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
                print('Loading multilingual encoder (first time only)...')
                cls._encoder = SentenceTransformer(
                    'paraphrase-multilingual-MiniLM-L12-v2')
                print('Encoder ready!')
            except ImportError:
                cls._encoder = 'unavailable'
        return cls._encoder if cls._encoder != 'unavailable' else None

    def __init__(self, text: str, category: str = 'general'):
        self.text     = text
        self.category = category
        self.vector   = None
        s = text.lower().strip()
        self.atom_id  = hashlib.md5(s.encode()).hexdigest()[:12]

    def encode(self):
        if self.vector is not None:
            return self.vector
        encoder = self._get_encoder()
        if encoder:
            self.vector = encoder.encode(self.text).tolist()
        else:
            # Fallback: simple hash-based pseudo-vector
            import hashlib, numpy as np
            seed = int(hashlib.md5(self.text.encode()).hexdigest(), 16) % (2**31)
            np.random.seed(seed)
            self.vector = np.random.randn(384).tolist()
        return self.vector

    def get_universal_meaning(self):
        v = self.encode()
        return [round(x, 4) for x in v[:5]]
