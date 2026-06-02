# KA-Mind Causal Mapper v2.4 (CPU Optimized)
import re
from .knowledge_atom import KnowledgeAtom, AtomType


class CausalMapper:

    _SENT_SPLIT = re.compile(r'(?<=[.!?।])\s+')
    _EFFECT_CAUSE = [
        re.compile(r'(.{5,100}?)\s+because\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+due to\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+since\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+क्योंकि\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
    ]
    _CAUSE_EFFECT = [
        re.compile(r'(.{5,100}?)\s+therefore\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+causes?\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+leads?\s+to\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+results?\s+in\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
        re.compile(r'(.{5,100}?)\s+इसलिए\s+(.{5,100}?)(?:[.।]|$)', re.IGNORECASE),
    ]

    def extract(self, text: str, domain: str = 'general',
                uid: str = 'system') -> list:
        atoms = []
        for sent in self._SENT_SPLIT.split(text):
            sent = sent.strip()
            if len(sent) < 15: continue

            # EFFECT ← CAUSE
            for pat in self._EFFECT_CAUSE:
                for m in pat.findall(sent):
                    if len(m) == 2:
                        effect, cause = m[0].strip(), m[1].strip()
                        if len(cause) > 4 and len(effect) > 4:
                            atoms.append(KnowledgeAtom(AtomType.CAUSAL,
                                {'cause': cause.lower(), 'effect': effect.lower(),
                                 'pattern': 'because', 'sentence': sent[:200]},
                                0.82, 'causal_extractor', domain, user_id=uid))

            # CAUSE → EFFECT
            for pat in self._CAUSE_EFFECT:
                for m in pat.findall(sent):
                    if len(m) == 2:
                        cause, effect = m[0].strip(), m[1].strip()
                        if len(cause) > 4 and len(effect) > 4:
                            atoms.append(KnowledgeAtom(AtomType.CAUSAL,
                                {'cause': cause.lower(), 'effect': effect.lower(),
                                 'pattern': 'causes', 'sentence': sent[:200]},
                                0.85, 'causal_extractor', domain, user_id=uid))
        return atoms
