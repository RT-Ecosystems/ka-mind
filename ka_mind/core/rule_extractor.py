# NeuraBrain Teacher — Layer B: Rule Extraction (CPU Optimized)
import re
from .knowledge_atom import KnowledgeAtom, AtomType


class RuleExtractor:
    _SENT_SPLIT = re.compile(r'(?<=[.!?।])\s+')
    _PATTERNS = [
        re.compile(r'(?:if|when|whenever|once|जब|अगर)\s+(.{5,100}?)(?:,\s*|\s+then\s+|\s+तो\s+)(.{5,100}?)(?:\.|$)', re.IGNORECASE),
        re.compile(r'(.{5,80}?)\s+(?:causes?|leads?\s+to|results?\s+in|produces?)\s+(.{5,80}?)(?:\.|$)', re.IGNORECASE),
        re.compile(r'(.{5,80}?)\s+always\s+(.{5,80}?)(?:\.|$)', re.IGNORECASE),
        re.compile(r'every\s+(.{5,80}?)\s+(?:is|has|can|will)\s+(.{5,80}?)(?:\.|$)', re.IGNORECASE),
        re.compile(r'(.{5,80}?)\s+(?:हमेशा|सदा)\s+(.{5,80}?)(?:\.|$)', re.IGNORECASE),
    ]

    def extract(self, text: str, domain: str = 'general',
                user_id: str = 'system') -> list:
        atoms = []
        for sent in self._SENT_SPLIT.split(text):
            sent = sent.strip()
            if len(sent) < 15: continue
            for pat in self._PATTERNS:
                for m in pat.findall(sent):
                    if len(m) == 2:
                        cond, conc = m[0].strip(), m[1].strip()
                        if len(cond) > 4 and len(conc) > 4:
                            atoms.append(KnowledgeAtom(AtomType.RULE,
                                {'condition': cond.lower(),
                                 'conclusion': conc.lower(),
                                 'sentence': sent[:200]},
                                0.85, 'extractor', domain, user_id=user_id))
        return atoms
