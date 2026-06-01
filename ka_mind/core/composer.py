# KA-Mind Composer v2.3 — Reasoning integrated
import random
from .knowledge_atom import AtomType
from .human_language_engine import HumanLanguageEngine
from .reasoning_engine import ReasoningEngine


class Composer:
    def __init__(self, graph_memory):
        self.memory   = graph_memory
        self.lang     = HumanLanguageEngine()
        self.reasoner = ReasoningEngine(graph_memory)

    def compose_answer(self, query: str, relevant_atoms: list,
                       style: str = 'auto') -> str:
        if not relevant_atoms:
            # Try reasoning even without direct matches
            reasoned = self.reasoner.reason(query)
            if reasoned:
                return reasoned
            return self.lang.generate(query, [], style)

        sorted_atoms = sorted(relevant_atoms,
                              key=lambda a: a.confidence, reverse=True)

        # Base answer from language engine
        answer = self.lang.generate(query, sorted_atoms[:8], style)

        # Enrich with formal reasoning
        logical = self.reasoner.reason(query)
        if logical and logical not in answer:
            answer += f' {logical}'

        return answer

    def compose_creative(self, query: str, atoms: list) -> str:
        return self.lang.generate(query, atoms, style='creative')

    def chain_reason(self, premise: str, steps: int = 4) -> list:
        chain = self.reasoner.causal_chain(premise, depth=steps)
        if len(chain) <= 1:
            derived = self.reasoner.forward_chain(max_steps=2)
            return [premise] + derived[:2] if derived else [premise]
        return chain

    def analogical_reason(self, query: str) -> str:
        similar = self.memory.search_scored(query, top_k=5)
        if similar:
            atoms = [a for a, _ in similar]
            return self.lang.generate(query, atoms, 'conversational')
        logical = self.reasoner.reason(query)
        return logical or self.lang.generate(query, [], 'conversational')
