# KA-Mind Core: Graph Memory
# BUG FIXED: Added real graph edges + retrieve_context() method
# BUG FIXED: Privacy-aware search


class GraphMemory:
    def __init__(self):
        self.graph = {}           # atom_id -> KnowledgeAtom
        self.edges = {}           # atom_id -> [{target, relation, strength}]

    def add_atom(self, atom) -> bool:
        if atom.atom_id in self.graph:
            self.graph[atom.atom_id].usage_count += 1
            existing = self.graph[atom.atom_id]
            existing.confidence = min(1.0, existing.confidence * 1.02)
            return False
        self.graph[atom.atom_id] = atom
        self.edges[atom.atom_id] = []
        return True

    def add_edge(self, from_id: str, to_id: str,
                 relation: str = 'related', strength: float = 1.0):
        if from_id in self.edges and to_id in self.graph:
            self.edges[from_id].append({'target': to_id,
                                        'relation': relation,
                                        'strength': strength})
            if from_id in self.graph:
                self.graph[from_id].connect(to_id, relation, strength)

    # BUG2 FIXED: retrieve_context was missing — now implemented
    def retrieve_context(self, start_atom_id: str, depth: int = 2):
        if start_atom_id not in self.graph:
            return []
        visited = set()
        frontier = [start_atom_id]
        results  = []
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
        qwords  = set(query.lower().split())
        results = []
        for atom in self.graph.values():
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
