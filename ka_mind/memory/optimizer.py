# KA-Mind Memory Optimizer
from ka_mind.core.knowledge_atom import AtomType


class MemoryRanker:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def rank_memories(self) -> str:
        for atom in self.memory.graph.values():
            evidence_score = atom.usage_count * 0.08
            atom.confidence = min(1.0, atom.confidence + evidence_score)
            if atom.confidence >= 0.8:
                atom.memory_type = 'Long-term'
            elif atom.confidence >= 0.4:
                atom.memory_type = 'Short-term'
            else:
                atom.memory_type = 'Temporary'
        return f'Ranked {len(self.memory.graph)} atoms.'

    def prune_weak(self, threshold: float = 0.2) -> int:
        to_delete = [aid for aid, a in self.memory.graph.items()
                     if a.confidence < threshold]
        for aid in to_delete:
            del self.memory.graph[aid]
            if aid in self.memory.edges:
                del self.memory.edges[aid]
        return len(to_delete)
