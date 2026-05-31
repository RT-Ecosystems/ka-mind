# KA-Mind Core: Knowledge Atom
# Technique: NeuraBrain
# BUG FIXED: Added CONCEPT, CAUSAL, PATTERN, PROCEDURE, ANALOGY
import hashlib, json, time
from enum import Enum


class AtomType(Enum):
    FACT      = 'fact'
    RULE      = 'rule'
    CONCEPT   = 'concept'    # BUG1 FIXED: was missing!
    CAUSAL    = 'causal'     # cause -> effect relationships
    PATTERN   = 'pattern'    # recurring structures
    PROCEDURE = 'procedure'  # step-by-step knowledge
    ANALOGY   = 'analogy'    # A:B as C:D


class KnowledgeAtom:
    def __init__(self, atom_type: AtomType, content: dict,
                 confidence: float = 1.0, source: str = 'internal',
                 category: str = 'general', scope: str = 'public',
                 user_id: str = 'system'):
        self.atom_type   = atom_type
        self.content     = content
        self.confidence  = confidence
        self.source      = source
        self.category    = category
        self.scope       = scope
        self.user_id     = user_id
        self.usage_count = 1
        self.last_accessed = time.time()
        self.connections = []   # NEW: graph edges to other atom_ids
        self.memory_type = 'Short-term (Active)'
        s = json.dumps(self.content, sort_keys=True, default=str)
        s += self.scope + self.user_id
        self.atom_id = hashlib.md5(s.encode()).hexdigest()[:12]

    def connect(self, other_id: str, relation: str = 'related', strength: float = 1.0):
        self.connections.append({'target': other_id, 'relation': relation, 'strength': strength})

    def to_text(self) -> str:
        c = self.content
        t = self.atom_type
        if t == AtomType.FACT:
            subj = c.get('subject', c.get('text', '?'))
            pred = c.get('predicate', 'is')
            obj  = c.get('object', '')
            return f'{subj} {pred} {obj}'.strip()
        if t == AtomType.RULE:
            cond = c.get('condition', c.get('text','?'))
            conc = c.get('conclusion', '')
            return f'If {cond} then {conc}'.strip()
        if t == AtomType.CAUSAL:
            cause  = c.get('cause', '?')
            effect = c.get('effect', '?')
            return f'{cause} causes {effect}'
        if t == AtomType.CONCEPT:
            name = c.get('name', c.get('text', '?'))
            defn = c.get('description', c.get('definition', ''))
            return f'{name}: {defn}'.strip()
        return c.get('text', json.dumps(c, default=str))

    def to_dict(self):
        return {'id': self.atom_id, 'type': self.atom_type.value,
                'content': self.content, 'confidence': self.confidence,
                'scope': self.scope, 'user_id': self.user_id}

    def __repr__(self):
        return f'KA[{self.atom_type.value[:4].upper()}:{self.atom_id}|{self.confidence:.2f}]'
