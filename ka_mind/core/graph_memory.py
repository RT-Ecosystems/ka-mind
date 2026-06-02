# KA-Mind Core: Graph Memory (CPU Optimized)
import time
from .knowledge_atom import AtomType

class GraphMemory:
    def __init__(self):
        self.graph = {}
        self.edges = {}
        from .graph_index import GraphIndex
        self.graph_index = GraphIndex()
        self._use_faiss = self.graph_index.is_available()

    def add_atom(self, atom) -> bool:
        if atom.atom_id in self.graph:
            self.graph[atom.atom_id].usage_count += 1
            existing = self.graph[atom.atom_id]
            existing.confidence = min(1.0, existing.confidence * 1.02)
            return False
        self.graph[atom.atom_id] = atom
        self.edges[atom.atom_id] = []
        # Also add to FAISS index for fast search
        if self._use_faiss and hasattr(atom, 'embedding') and atom.embedding is not None:
            self.graph_index.add(atom.atom_id, atom.embedding)
        return True

    def add_relation(self, from_id: str, to_id: str,
                     relation: str = 'related', strength: float = 1.0):
        self.add_edge(from_id, to_id, relation, strength)

    def add_edge(self, from_id: str, to_id: str,
                 relation: str = 'related', strength: float = 1.0):
        if from_id in self.edges and to_id in self.graph:
            self.edges[from_id].append({'target': to_id,
                                        'relation': relation,
                                        'strength': strength})
            if from_id in self.graph:
                self.graph[from_id].connect(to_id, relation, strength)

    def retrieve_context(self, start_atom_id: str, depth: int = 2):
        if start_atom_id not in self.graph:
            return []
        visited = set()
        frontier = [start_atom_id]
        results = []
        for _ in range(depth):
            next_frontier = []
            for aid in frontier:
                if aid in visited or aid not in self.graph:
                    continue
                visited.add(aid)
                atom = self.graph[aid]
                results.append((aid, atom.to_dict()))
                for edge in self.edges.get(aid, []):
                    if edge['target'] not in visited:
                        next_frontier.append(edge['target'])
            frontier = next_frontier
        return results

    def search(self, keyword: str, current_user_id: str = 'system',
               top_k: int = 10) -> list:
        results = []
        kw = keyword.lower()
        for atom in self.graph.values():
            text = atom.to_text().lower()
            if kw in text:
                if atom.scope == 'public' or atom.user_id == current_user_id:
                    score = text.count(kw) * atom.confidence
                    results.append((score, atom))
        results.sort(key=lambda x: x[0], reverse=True)
        return [a for _, a in results[:top_k]]

    def search_scored(self, query: str, current_user_id: str = 'system',
                      top_k: int = 15) -> list:
        # Try FAISS semantic search first
        if self._use_faiss and self.graph_index.size > 0:
            try:
                from .vector_atom import VectorAtom
                va = VectorAtom(query)
                qv = va.encode()
                faiss_results = self.graph_index.search(qv, top_k * 2)
                if faiss_results:
                    results = []
                    for atom_id, score in faiss_results:
                        if atom_id in self.graph:
                            atom = self.graph[atom_id]
                            if atom.scope == 'public' or atom.user_id == current_user_id:
                                results.append((atom, float(score) * atom.confidence))
                    if results:
                        results.sort(key=lambda x: x[1], reverse=True)
                        return results[:top_k]
            except Exception:
                pass  # Fall back to keyword search

        # Keyword-based search (fallback)
        qwords = set(query.lower().split())
        results = []
        graph = self.graph
        for atom in graph.values():
            if atom.scope != 'public' and atom.user_id != current_user_id:
                continue
            awords = set(atom.to_text().lower().split())
            overlap = len(qwords & awords)
            if overlap > 0:
                score = overlap / max(len(qwords), 1) * atom.confidence
                results.append((score, atom))
        results.sort(key=lambda x: x[0], reverse=True)
        return [(a, s) for s, a in results[:top_k]]

    def memory_stats(self) -> str:
        pub  = sum(1 for a in self.graph.values() if a.scope == 'public')
        priv = sum(1 for a in self.graph.values() if a.scope == 'private')
        edges_count = sum(len(e) for e in self.edges.values())
        return (f'Total: {len(self.graph)} Atoms '
                f'(Public: {pub}, Private: {priv}) | Edges: {edges_count}')
