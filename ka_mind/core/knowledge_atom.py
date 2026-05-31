"""
Knowledge Atom - Updated with Scope and User_ID for Privacy.
"""
import hashlib
import json
import time
from enum import Enum

class AtomType(Enum):
    FACT = "fact"
    RULE = "rule"

class KnowledgeAtom:
    def __init__(self, atom_type: AtomType, content: dict, confidence: float = 1.0, 
                 source: str = "internal", category: str = "general", 
                 scope: str = "public", user_id: str = "system"):
        self.atom_type = atom_type
        self.content = content
        self.confidence = confidence
        self.source = source
        self.category = category
        self.scope = scope          # 'public' या 'private'
        self.user_id = user_id      # किस यूज़र का डेटा है?
        
        self.usage_count = 1
        self.last_accessed = time.time()
        
        # Hash बनाते समय scope और user_id को भी ध्यान में रखेंगे ताकि प्राइवेट और पब्लिक डेटा मिक्स न हो
        s = json.dumps(self.content, sort_keys=True) + self.scope + self.user_id
        self.atom_id = hashlib.md5(s.encode()).hexdigest()[:12]

    def to_dict(self):
        return {
            "id": self.atom_id, "content": self.content, 
            "scope": self.scope, "user_id": self.user_id
        }
