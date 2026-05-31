# KA-Mind Vector Graph — Semantic search
# BUG FIXED: Works with lazy VectorAtom
from ka_mind.core.vector_atom import VectorAtom


class VectorGraph:
    def __init__(self):
        self.graph = {}

    def add_atom(self, atom: VectorAtom):
        atom.encode()  # encode now, store vector
        self.graph[atom.atom_id] = atom

    def search_by_meaning(self, query: str, top_k: int = 5):
        if not self.graph:
            return None, 0.0
        encoder = VectorAtom._get_encoder()
        if encoder is None:
            # Fallback: text search
            qw = set(query.lower().split())
            best, best_score = None, 0.0
            for atom in self.graph.values():
                aw = set(atom.text.lower().split())
                s  = len(qw & aw) / max(len(qw), 1)
                if s > best_score: best_score = s; best = atom
            return best, best_score
        import numpy as np
        qv = encoder.encode(query)
        best, best_score = None, 0.0
        for atom in self.graph.values():
            if atom.vector is None: continue
            av  = np.array(atom.vector)
            cos = float(np.dot(qv, av) / (np.linalg.norm(qv)*np.linalg.norm(av)+1e-9))
            if cos > best_score: best_score = cos; best = atom
        return best, best_score

    def search_top_k(self, query: str, k: int = 5):
        encoder = VectorAtom._get_encoder()
        if encoder is None or not self.graph: return []
        import numpy as np
        qv = encoder.encode(query)
        scored = []
        for atom in self.graph.values():
            if atom.vector is None: continue
            av  = np.array(atom.vector)
            cos = float(np.dot(qv,av)/(np.linalg.norm(qv)*np.linalg.norm(av)+1e-9))
            scored.append((cos, atom))
        scored.sort(reverse=True)
        return [(a, s) for s, a in scored[:k]]
