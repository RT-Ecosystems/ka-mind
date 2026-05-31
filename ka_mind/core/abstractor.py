# KA-Mind Abstractor — Knowledge Compression
# BUG FIXED: AtomType.CONCEPT now exists
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class Abstractor:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def create_concepts(self) -> list:
        concepts_created = []
        subjects_count   = {}

        for atom in self.memory.graph.values():
            text = atom.to_text().lower()
            words = text.split()
            if len(words) >= 2:
                subj = words[0].strip()
                if len(subj) > 2 and not subj.isdigit():
                    subjects_count[subj] = subjects_count.get(subj, 0) + 1

        for subject, count in subjects_count.items():
            if count >= 3:
                exists = any(
                    a.atom_type == AtomType.CONCEPT
                    and a.content.get('name') == subject
                    for a in self.memory.graph.values())
                if not exists:
                    # BUG1 FIXED: AtomType.CONCEPT now valid!
                    concept_atom = KnowledgeAtom(
                        atom_type = AtomType.CONCEPT,
                        content   = {
                            'name': subject,
                            'description': f'Concept derived from {count} facts.',
                            'evidence_count': count
                        },
                        confidence = min(0.5 + count * 0.05, 1.0),
                        category   = 'concept'
                    )
                    if self.memory.add_atom(concept_atom):
                        concepts_created.append(
                            f'Concept created: [{subject}] from {count} facts')
        return concepts_created
