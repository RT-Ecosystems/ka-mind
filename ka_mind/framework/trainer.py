"""
KaTrainer - किसी भी KaModel को कच्चा डेटा खिलाकर ट्रेन करने वाला इंजन।
"""
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class KaTrainer:
    def __init__(self, model):
        self.model = model

    def train_from_text(self, text_data: str):
        print(f"🎓 [Trainer]: '{self.model.name}' मॉडल की ट्रेनिंग शुरू हो रही है...")
        sentences = re.split(r'(?<=[.!?]) +', text_data)
        atoms_added = 0
        
        for sentence in sentences:
            if len(sentence) > 10:
                atom = KnowledgeAtom(
                    atom_type=AtomType.FACT, 
                    content={"text": sentence}, 
                    source="training_data", 
                    category=self.model.domain
                )
                if self.model.memory.add_atom(atom):
                    atoms_added += 1
                    
        print(f"✅ ट्रेनिंग पूरी! {atoms_added} नए Atoms '{self.model.name}' के दिमाग में सेव हो गए।")
        return atoms_added
