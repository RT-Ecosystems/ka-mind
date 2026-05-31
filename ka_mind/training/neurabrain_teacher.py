# NeuraBrain Teacher Script — 3 Layers
# Layer A: Facts (accuracy)
# Layer B: Rules (imagination)
# Layer C: Causality (deep reasoning)
# This is the core of NeuraBrain technique
from ka_mind.core.fact_extractor import FactExtractor
from ka_mind.core.rule_extractor import RuleExtractor
from ka_mind.core.causal_mapper  import CausalMapper
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class NeuraBrainTeacher:
    def __init__(self, graph_memory, vector_graph=None):
        self.memory          = graph_memory
        self.vector_graph    = vector_graph
        self.fact_extractor  = FactExtractor()
        self.rule_extractor  = RuleExtractor()
        self.causal_mapper   = CausalMapper()
        self._chunks         = 0
        self._atoms_created  = 0

    def process_chunk(self, text: str, domain: str = 'general',
                      uid: str = 'system') -> int:
        before = len(self.memory.graph)

        # Layer A: Extract facts
        for atom in self.fact_extractor.extract(text, domain, uid):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)

        # Layer B: Extract rules
        for atom in self.rule_extractor.extract(text, domain, uid):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)

        # Layer C: Extract causal relationships
        for atom in self.causal_mapper.extract(text, domain, uid):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)

        # Build edges between related atoms (graph connections)
        self._build_edges(text)

        self._chunks += 1
        created = len(self.memory.graph) - before
        self._atoms_created += created
        return created

    def _add_to_vector(self, atom):
        # BUG4 FIX: VectorGraph is now populated during training
        if self.vector_graph is not None:
            try:
                from ka_mind.core.vector_atom import VectorAtom
                va = VectorAtom(atom.to_text(), atom.category)
                self.vector_graph.add_atom(va)
            except Exception:
                pass  # Graceful fallback if model unavailable

    def _build_edges(self, text: str):
        atoms = list(self.memory.graph.values())[-50:]
        for i, a1 in enumerate(atoms):
            for a2 in atoms[i+1:]:
                t1 = set(a1.to_text().lower().split())
                t2 = set(a2.to_text().lower().split())
                overlap = len(t1 & t2) / max(len(t1 | t2), 1)
                if overlap > 0.3:
                    self.memory.add_edge(a1.atom_id, a2.atom_id, 'related', overlap)

    @property
    def stats(self) -> dict:
        return {'chunks': self._chunks, 'atoms_created': self._atoms_created,
                'total_atoms': len(self.memory.graph)}
