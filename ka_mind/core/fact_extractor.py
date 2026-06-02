# NeuraBrain Teacher — Layer A: Fact Extraction (CPU Optimized)
import re
from .knowledge_atom import KnowledgeAtom, AtomType


class FactExtractor:
    # Precompiled patterns
    _IS_PAT = [
        re.compile(r'(\w[\w\s]{1,40}?)\s+is(?:\s+the|\s+a|\s+an)?\s+([\w][\w\s]{1,60}?)(?:\.|,|;|$)', re.IGNORECASE),
        re.compile(r'(\w[\w\s]{1,40}?)\s+are(?:\s+the|\s+a)?\s+([\w][\w\s]{1,60}?)(?:\.|,|;|$)', re.IGNORECASE),
        re.compile(r'(\w[\w\s]{1,40}?)\s+was\s+([\w][\w\s]{1,60}?)(?:\.|,|;|$)', re.IGNORECASE),
    ]
    _HAS_PAT = [
        re.compile(r'(\w[\w\s]{1,40}?)\s+has\s+([\w][\w\s]{1,60}?)(?:\.|,|;|$)', re.IGNORECASE),
        re.compile(r'(\w[\w\s]{1,40}?)\s+contains\s+([\w][\w\s]{1,60}?)(?:\.|,|;|$)', re.IGNORECASE),
    ]
    _DEF_PAT = [
        re.compile(r'(\w[\w\s]{1,30}?)\s+(?:is defined as|means|refers to|एक है|होता है)\s+(.{10,200}?)(?:\.|$)', re.IGNORECASE),
    ]

    # Sentence splitter (cached)
    _SENT_SPLIT = re.compile(r'(?<=[.!?।])\s+')

    def extract(self, text: str, domain: str = 'general',
                user_id: str = 'system') -> list:
        atoms = []
        for sent in self._SENT_SPLIT.split(text):
            sent = sent.strip()
            if len(sent) < 8: continue
            atoms += self._run(sent, self._IS_PAT,  'is',  0.88, domain, user_id)
            atoms += self._run(sent, self._HAS_PAT, 'has', 0.82, domain, user_id)
            atoms += self._defs(sent, domain, user_id)
            atoms += self._general(sent, domain, user_id)
        return atoms

    def _run(self, sent, patterns, pred, conf, domain, uid):
        out = []
        for pat in patterns:
            for m in pat.findall(sent):
                s, o = m[0].strip(), m[1].strip()
                if len(s) > 2 and len(o) > 2 and not s.isdigit():
                    out.append(KnowledgeAtom(AtomType.FACT,
                        {'subject': s.lower(), 'predicate': pred,
                         'object': o.lower(), 'sentence': sent[:180]},
                        conf, 'extractor', domain, user_id=uid))
        return out

    def _defs(self, sent, domain, uid):
        out = []
        for pat in self._DEF_PAT:
            for m in pat.findall(sent):
                t, d = m[0].strip(), m[1].strip()
                if len(t) > 2:
                    out.append(KnowledgeAtom(AtomType.CONCEPT,
                        {'name': t.lower(), 'definition': d, 'sentence': sent[:180]},
                        0.93, 'extractor', domain, user_id=uid))
        return out

    def _general(self, sent, domain, uid):
        words = sent.split()
        if 5 <= len(words) <= 50:
            return [KnowledgeAtom(AtomType.FACT,
                {'text': sent, 'subject': words[0].lower(),
                 'sentence': sent[:180]},
                0.75, 'extractor', domain, user_id=uid)]
        return []
