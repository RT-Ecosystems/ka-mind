"""
Abstractor - हज़ारों छोटे Atoms को मिलाकर एक बड़ा 'Concept' बनाना। (Knowledge Compression)
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class Abstractor:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def create_concepts(self) -> list:
        """समान प्रकार के फैक्ट्स को मिलाकर एक बड़ा कांसेप्ट बनाना"""
        concepts_created = []
        subjects_count = {}
        
        # 1. गिनना कि कौन सा विषय (Subject) सबसे ज्यादा बार आया है
        for atom in self.memory.graph.values():
            text = atom.content.get("text", "").lower()
            if " " in text:
                subject = text.split(" ")[0].strip()  # वाक्य का पहला शब्द (जैसे: कुत्ता, सूरज)
                if len(subject) > 2:
                    subjects_count[subject] = subjects_count.get(subject, 0) + 1
                    
        # 2. अगर कोई विषय 3 से ज्यादा बार आया है, तो उसका एक Concept Atom बनाओ
        for subject, count in subjects_count.items():
            if count >= 3:
                # चेक करो कि क्या इसका कांसेप्ट पहले से है
                concept_exists = any(a.category == "concept" and a.content.get("name") == subject for a in self.memory.graph.values())
                
                if not concept_exists:
                    concept_atom = KnowledgeAtom(
                        atom_type=AtomType.CONCEPT,
                        content={"name": subject, "description": f"A generalized concept derived from {count} specific facts."},
                        category="concept"
                    )
                    self.memory.add_atom(concept_atom)
                    concepts_created.append(f"🌌 [Concept Creation]: '{subject}' के बारे में बहुत डेटा मिला। नया Concept बनाया गया!")
                    
        return concepts_created
