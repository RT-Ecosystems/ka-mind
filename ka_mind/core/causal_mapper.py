# KA-Mind Causal Mapper v2.3.1
# HOTFIX: 'because' pattern was storing cause/effect BACKWARDS
# 'Water heats BECAUSE sun shines' → cause=sun shines, effect=water heats
import re
from .knowledge_atom import KnowledgeAtom, AtomType


class CausalMapper:

    # (effect, cause) — because/due to/since → group1 is effect, group2 is cause
    EFFECT_CAUSE = [
        r'(.{5,100}?)\s+because\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+due to\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+since\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+क्योंकि\s+(.{5,100}?)(?:[.।]|$)',
    ]

    # (cause, effect) — therefore/causes/leads to → group1 is cause, group2 is effect
    CAUSE_EFFECT = [
        r'(.{5,100}?)\s+therefore\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+causes?\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+leads?\s+to\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+results?\s+in\s+(.{5,100}?)(?:[.।]|$)',
        r'(.{5,100}?)\s+इसलिए\s+(.{5,100}?)(?:[.।]|$)',
    ]

    def extract(self, text: str, domain: str = 'general',
                uid: str = 'system') -> list:
        atoms = []
        for sent in re.split(r'(?<=[.!?।])\s+', text):
            sent = sent.strip()
            if len(sent) < 15: continue

            # EFFECT ← CAUSE patterns (because/due to/since)
            for pat in self.EFFECT_CAUSE:
                for m in re.findall(pat, sent, re.IGNORECASE):
                    if len(m) == 2:
                        effect, cause = m[0].strip(), m[1].strip()  # FIXED ORDER
                        if len(cause) > 4 and len(effect) > 4:
                            atoms.append(KnowledgeAtom(AtomType.CAUSAL,
                                {'cause':  cause.lower(),
                                 'effect': effect.lower(),
                                 'pattern': 'because',
                                 'sentence': sent[:200]},
                                0.82, 'causal_extractor', domain, user_id=uid))

            # CAUSE → EFFECT patterns (therefore/causes/leads to)
            for pat in self.CAUSE_EFFECT:
                for m in re.findall(pat, sent, re.IGNORECASE):
                    if len(m) == 2:
                        cause, effect = m[0].strip(), m[1].strip()  # CORRECT ORDER
                        if len(cause) > 4 and len(effect) > 4:
                            atoms.append(KnowledgeAtom(AtomType.CAUSAL,
                                {'cause':  cause.lower(),
                                 'effect': effect.lower(),
                                 'pattern': 'causes',
                                 'sentence': sent[:200]},
                                0.85, 'causal_extractor', domain, user_id=uid))
        return atoms
