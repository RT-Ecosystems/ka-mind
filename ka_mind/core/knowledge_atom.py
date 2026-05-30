"""
Knowledge Atom - Upgraded with Category, Usage tracking, and Decay.
"""
import hashlib
import json
import time
from enum import Enum

class AtomType(Enum):
    FACT = "fact"
    RULE = "rule"
    CAUSAL = "causal"
    CONCEPT = "concept"

class KnowledgeAtom:
    def __init__(self, atom_type: AtomType, content: dict, confidence: float = 1.0, source: str = "internal", category: str = "general"):
        self.atom_type = atom_type
        self.content = content
        self.confidence = confidence
        self.source = source
        self.category = category
        
        self.usage_count = 1
        self.last_accessed = time.time()
        self.status = "active" # active या archived (Cold Storage)
        
        s = json.dumps(self.content, sort_keys=True)
        self.atom_id = hashlib.md5(s.encode()).hexdigest()[:12]

    def access(self):
        """जब भी एटम काम आएगा, इसकी ताकत बढ़ जाएगी"""
        self.usage_count += 1
        self.last_accessed = time.time()
        if self.confidence < 1.0:
            self.confidence = min(1.0, self.confidence + 0.1)

    def to_dict(self):
        return {
            "id": self.atom_id, 
            "type": self.atom_type.value, 
            "content": self.content, 
            "confidence": round(self.confidence, 2),
            "source": self.source,
            "category": self.category,
            "usage_count": self.usage_count,
            "status": self.status
        }
