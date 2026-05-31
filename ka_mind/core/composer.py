# KA-Mind Composer — Upgraded with HumanLanguageEngine
# NeuraBrain: Knowledge -> Human-like Language
import random
from .knowledge_atom import AtomType
from .human_language_engine import HumanLanguageEngine


class Composer:
    def __init__(self, graph_memory):
        self.memory  = graph_memory
        self.lang    = HumanLanguageEngine()

    def compose_answer(self, query: str, relevant_atoms: list,
                       style: str = 'auto') -> str:
        if not relevant_atoms:
            return self.lang.generate(query, [], style)

        # Sort by confidence, most confident first
        sorted_atoms = sorted(relevant_atoms,
                              key=lambda a: a.confidence, reverse=True)

        # Use HumanLanguageEngine for natural output
        return self.lang.generate(query, sorted_atoms[:8], style)

    def compose_creative(self, query: str,
                         relevant_atoms: list) -> str:
        return self.lang.generate(query, relevant_atoms, style='creative')

    def _apply_rules(self, query: str, rules: list) -> list:
        qw  = set(query.lower().split())
        out = []
        for rule in rules:
            cond = rule.content.get('condition', '')
            cw   = set(cond.split())
            if len(qw & cw) / max(len(cw), 1) > 0.3:
                conc = rule.content.get('conclusion', '')
                out.append(f'if {cond} then {conc}')
        return out

    def chain_reason(self, premise: str, steps: int = 4) -> list:
        chain   = [premise]
        current = premise
        for _ in range(steps):
            related = self.memory.search_scored(current, top_k=5)
            if not related: break
            rules = [a for a, _ in related
                     if a.atom_type == AtomType.RULE]
            applied = self._apply_rules(current, rules)
            if not applied: break
            if applied[0] == current: break
            chain.append(f'  -> {applied[0]}')
            current = applied[0]
        return chain

    def analogical_reason(self, query: str) -> str:
        similar = self.memory.search_scored(query, top_k=5)
        if similar:
            atoms = [a for a, _ in similar]
            return self.lang.generate(query, atoms, 'conversational')
        return self.lang.generate(query, [], 'conversational')
