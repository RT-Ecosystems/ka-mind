# KA-Mind Composer — Imagination Engine
# Combines rules + facts to answer UNSEEN questions
from .knowledge_atom import AtomType


class Composer:
    def __init__(self, graph_memory):
        self.memory = graph_memory

    def compose_answer(self, query: str, relevant_atoms: list) -> str:
        facts    = [a for a in relevant_atoms if a.atom_type == AtomType.FACT]
        rules    = [a for a in relevant_atoms if a.atom_type == AtomType.RULE]
        causal   = [a for a in relevant_atoms if a.atom_type == AtomType.CAUSAL]
        concepts = [a for a in relevant_atoms if a.atom_type == AtomType.CONCEPT]
        parts    = []
        for a in concepts[:2]: parts.append(a.to_text())
        for a in facts[:4]:    parts.append(a.to_text())
        for a in causal[:2]:   parts.append(a.to_text())
        reasoned = self._apply_rules(query, rules)
        parts.extend(reasoned[:2])
        if not parts:
            return self._analogical_reason(query)
        return ' | '.join(p for p in parts if p.strip())

    def _apply_rules(self, query: str, rules: list) -> list:
        qw  = set(query.lower().split())
        out = []
        for rule in rules:
            cond = rule.content.get('condition', '')
            cw   = set(cond.split())
            overlap = len(qw & cw) / max(len(cw), 1)
            if overlap > 0.3:
                conc = rule.content.get('conclusion', '')
                out.append(f'Based on rule: if {cond} then {conc}')
        return out

    def _analogical_reason(self, query: str) -> str:
        similar = self.memory.search_scored(query, top_k=3)
        if similar:
            texts = [a.to_text() for a, _ in similar]
            return 'Related knowledge: ' + ' | '.join(texts)
        return 'Insufficient knowledge. Please train on more data for this domain.'

    def chain_reason(self, premise: str, steps: int = 4) -> list:
        chain   = [premise]
        current = premise
        for _ in range(steps):
            related = self.memory.search_scored(current, top_k=5)
            if not related: break
            rules = [a for a, _ in related if a.atom_type == AtomType.RULE]
            applied = self._apply_rules(current, rules)
            if not applied: break
            conclusion = applied[0].replace('Based on rule: ', '')
            if conclusion == current: break
            chain.append(f'  -> {conclusion}')
            current = conclusion
        return chain
