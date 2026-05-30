"""
Knowledge Atom - ज्ञान की बुनियादी, अर्थपूर्ण इकाई
"""
import hashlib
import json
from enum import Enum

class AtomType(Enum):
    FACT = "fact"           # जैसे: "सेब एक फल है"
    RULE = "rule"           # जैसे: "अगर बारिश होगी, तो जमीन गीली होगी"
    CAUSAL = "causal"       # जैसे: "गुरुत्वाकर्षण के कारण चीजें नीचे गिरती हैं"
    CONCEPT = "concept"     # जैसे: "AI की परिभाषा"

class KnowledgeAtom:
    def __init__(self, atom_type: AtomType, content: dict, confidence: float = 1.0, source: str = "internal"):
        self.atom_type = atom_type
        self.content = content  # Dictionary (e.g., {"subject": "Sun", "predicate": "is", "object": "Star"})
        self.confidence = confidence
        self.source = source
        
        # Atom के कंटेंट से एक यूनीक ID बनाना (ताकि कोई डुप्लीकेट ज्ञान न रहे)
        s = json.dumps(self.content, sort_keys=True)
        self.atom_id = hashlib.md5(s.encode()).hexdigest()[:12]

    def to_dict(self):
        return {
            "id": self.atom_id, 
            "type": self.atom_type.value, 
            "content": self.content, 
            "confidence": self.confidence,
            "source": self.source
        }

    def __repr__(self):
        return f"Atom[{self.atom_type.name} | {self.atom_id}]"
