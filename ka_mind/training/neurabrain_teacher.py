# NeuraBrain Teacher Script v2.3
# Ethics from true_teacher.py merged in (true_teacher.py deprecated)
from ka_mind.core.fact_extractor  import FactExtractor
from ka_mind.core.rule_extractor  import RuleExtractor
from ka_mind.core.causal_mapper   import CausalMapper
from ka_mind.core.knowledge_atom  import KnowledgeAtom, AtomType

ETHICS_RULES = [
    {'condition': 'user asks harmful content', 'conclusion': 'refuse and explain why'},
    {'condition': 'user shares private data', 'conclusion': 'protect privacy, do not store'},
    {'condition': 'information is uncertain', 'conclusion': 'say I am not sure'},
    {'condition': 'user needs help urgently', 'conclusion': 'prioritize safety response'},
]


class NeuraBrainTeacher:
    def __init__(self, graph_memory, vector_graph=None):
        self.memory          = graph_memory
        self.vector_graph    = vector_graph
        self.fact_extractor  = FactExtractor()
        self.rule_extractor  = RuleExtractor()
        self.causal_mapper   = CausalMapper()
        self._chunks         = 0
        self._atoms_created  = 0
        self._teach_ethics()

    def _teach_ethics(self):
        for rule_data in ETHICS_RULES:
            atom = KnowledgeAtom(AtomType.RULE, rule_data,
                                 confidence=1.0, category='ethics')
            self.memory.add_atom(atom)

    def process_chunk(self, text: str, domain: str = 'general',
                      uid: str = 'system') -> int:
        before = len(self.memory.graph)
        for atom in self.fact_extractor.extract(text, domain, uid):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)
        for atom in self.rule_extractor.extract(text, domain, uid):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)
        for atom in self.causal_mapper.extract(text, domain, uid):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)
        self._build_edges()
        self._chunks += 1
        created = len(self.memory.graph) - before
        self._atoms_created += created
        return created

    def _add_to_vector(self, atom):
        if self.vector_graph is None: return
        try:
            from ka_mind.core.vector_atom import VectorAtom
            va = VectorAtom(atom.to_text(), atom.category)
            self.vector_graph.add_atom(va)
        except Exception: pass

    def _build_edges(self):
        atoms = list(self.memory.graph.values())[-30:]
        for i, a1 in enumerate(atoms):
            for a2 in atoms[i+1:]:
                t1 = set(a1.to_text().lower().split())
                t2 = set(a2.to_text().lower().split())
                overlap = len(t1 & t2) / max(len(t1 | t2), 1)
                if overlap > 0.35:
                    self.memory.add_edge(a1.atom_id, a2.atom_id, 'related', overlap)

    @property
    def stats(self):
        return {'chunks': self._chunks, 'atoms': self._atoms_created,
                'total': len(self.memory.graph)}
