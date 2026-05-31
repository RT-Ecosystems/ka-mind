# NeuraBrain Teacher — Layer C: Causal Mapping
# Extracts WHY/BECAUSE relationships (enables deep REASONING)
import re
from .knowledge_atom import KnowledgeAtom, AtomType


class CausalMapper:
    PATTERNS = [
        r'(.{5,100}?)\s+because\s+(.{5,100}?)(?:\.|$)',
        r'(.{5,100}?)\s+due to\s+(.{5,100}?)(?:\.|$)',
        r'(.{5,100}?)\s+therefore\s+(.{5,100}?)(?:\.|$)',
        r'(.{5,100}?)\s+since\s+(.{5,100}?)(?:\.|$)',
        r'(.{5,100}?)\s+क्योंकि\s+(.{5,100}?)(?:\।|$)',
        r'(.{5,100}?)\s+इसलिए\s+(.{5,100}?)(?:\।|$)',
    ]

    def extract(self, text: str, domain: str = 'general',
                uid: str = 'system') -> list:
        atoms = []
        for sent in re.split(r'(?<=[.!?।])\s+', text):
            sent = sent.strip()
            if len(sent) < 15: continue
            for pat in self.PATTERNS:
                for m in re.findall(pat, sent, re.IGNORECASE):
                    if len(m) == 2:
                        p1, p2 = m[0].strip(), m[1].strip()
                        if len(p1) > 5 and len(p2) > 5:
                            atoms.append(KnowledgeAtom(AtomType.CAUSAL,
                                {'cause': p1.lower(), 'effect': p2.lower(),
                                 'sentence': sent[:200]},
                                0.80, 'extractor', domain, user_id=uid))
        return atoms
