# NeuraBrain Teacher — Layer B: Rule Extraction
# Extracts IF-THEN rules (enables IMAGINATION)
import re
from .knowledge_atom import KnowledgeAtom, AtomType


class RuleExtractor:
    PATTERNS = [
        r'(?:if|when|whenever|once|जब|अगर)\s+(.{5,100}?)(?:,\s*|\s+then\s+|\s+तो\s+)(.{5,100}?)(?:\.|$)',
        r'(.{5,80}?)\s+(?:causes?|leads?\s+to|results?\s+in|produces?)\s+(.{5,80}?)(?:\.|$)',
        r'(.{5,80}?)\s+always\s+(.{5,80}?)(?:\.|$)',
        r'every\s+(.{5,80}?)\s+(?:is|has|can|will)\s+(.{5,80}?)(?:\.|$)',
        r'(.{5,80}?)\s+(?:हमेशा|सदा)\s+(.{5,80}?)(?:\.|$)',
    ]

    def extract(self, text: str, domain: str = 'general',
                user_id: str = 'system') -> list:
        atoms = []
        for sent in re.split(r'(?<=[.!?।])\s+', text):
            sent = sent.strip()
            if len(sent) < 15: continue
            for pat in self.PATTERNS:
                for m in re.findall(pat, sent, re.IGNORECASE):
                    if len(m) == 2:
                        cond, conc = m[0].strip(), m[1].strip()
                        if len(cond) > 4 and len(conc) > 4:
                            atoms.append(KnowledgeAtom(AtomType.RULE,
                                {'condition': cond.lower(),
                                 'conclusion': conc.lower(),
                                 'sentence': sent[:200]},
                                0.85, 'extractor', domain, user_id=uid))
        return atoms

    def extract(self, text: str, domain: str = 'general',
                uid: str = 'system') -> list:
        atoms = []
        for sent in re.split(r'(?<=[.!?।])\s+', text):
            sent = sent.strip()
            if len(sent) < 15: continue
            for pat in self.PATTERNS:
                for m in re.findall(pat, sent, re.IGNORECASE):
                    if len(m) == 2:
                        cond, conc = m[0].strip(), m[1].strip()
                        if len(cond) > 4 and len(conc) > 4:
                            atoms.append(KnowledgeAtom(AtomType.RULE,
                                {'condition': cond.lower(),
                                 'conclusion': conc.lower(),
                                 'sentence': sent[:200]},
                                0.85, 'extractor', domain, user_id=uid))
        return atoms
