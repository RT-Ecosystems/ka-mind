"""
KnowledgePacks — Pre-built atoms for common knowledge domains.
Provides instant general knowledge without training on massive datasets.
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class KnowledgePack:
    """Factory for pre-built knowledge atoms."""

    @staticmethod
    def science_pack() -> list:
        """Basic science knowledge."""
        return [
            KnowledgeAtom(AtomType.FACT, {"subject": "water", "predicate": "is", "object": "H2O"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.FACT, {"subject": "sun", "predicate": "is", "object": "a star"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.FACT, {"subject": "earth", "predicate": "orbits", "object": "the sun"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.FACT, {"subject": "DNA", "predicate": "contains", "object": "genetic information"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.FACT, {"subject": "atoms", "predicate": "are", "object": "building blocks of matter"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.RULE, {"condition": "water freezes", "conclusion": "temperature is below 0°C"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.RULE, {"condition": "metal is heated", "conclusion": "it expands"}, 0.95, category="science"),
            KnowledgeAtom(AtomType.CAUSAL, {"cause": "gravity", "effect": "objects fall towards earth"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.CAUSAL, {"cause": "photosynthesis", "effect": "plants produce oxygen"}, 1.0, category="science"),
            KnowledgeAtom(AtomType.CONCEPT, {"name": "gravity", "definition": "force that attracts objects towards each other"}, 1.0, category="science"),
        ]

    @staticmethod
    def history_pack() -> list:
        """Basic world history knowledge."""
        return [
            KnowledgeAtom(AtomType.FACT, {"subject": "World War II", "predicate": "ended in", "object": "1945"}, 1.0, category="history"),
            KnowledgeAtom(AtomType.FACT, {"subject": "India", "predicate": "became independent in", "object": "1947"}, 1.0, category="history"),
            KnowledgeAtom(AtomType.FACT, {"subject": "internet", "predicate": "was invented in", "object": "the late 20th century"}, 0.95, category="history"),
            KnowledgeAtom(AtomType.CAUSAL, {"cause": "industrial revolution", "effect": "mass production became possible"}, 0.9, category="history"),
            KnowledgeAtom(AtomType.RULE, {"condition": "a country becomes independent", "conclusion": "it forms its own government"}, 0.9, category="history"),
        ]

    @staticmethod
    def geography_pack() -> list:
        """Basic geography knowledge."""
        return [
            KnowledgeAtom(AtomType.FACT, {"subject": "Pacific Ocean", "predicate": "is", "object": "the largest ocean"}, 1.0, category="geography"),
            KnowledgeAtom(AtomType.FACT, {"subject": "Mount Everest", "predicate": "is", "object": "the highest mountain"}, 1.0, category="geography"),
            KnowledgeAtom(AtomType.FACT, {"subject": "India", "predicate": "has", "object": "28 states and 8 union territories"}, 1.0, category="geography"),
            KnowledgeAtom(AtomType.FACT, {"subject": "Nile", "predicate": "is", "object": "the longest river"}, 0.95, category="geography"),
        ]

    @staticmethod
    def general_pack() -> list:
        """General knowledge — combination of all packs."""
        atoms = []
        atoms.extend(KnowledgePack.science_pack())
        atoms.extend(KnowledgePack.history_pack())
        atoms.extend(KnowledgePack.geography_pack())
        return atoms

    @classmethod
    def load_all(cls, graph_memory) -> int:
        """Load all knowledge packs into a graph memory. Returns number of atoms added."""
        atoms = cls.general_pack()
        count = 0
        for atom in atoms:
            if graph_memory.add_atom(atom):
                count += 1
        return count
