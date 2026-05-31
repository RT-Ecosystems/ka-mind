# KA-Mind World Model — Rule discovery + What-If simulation
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class WorldModel:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def discover_rules(self) -> list:
        rules_found = []
        rule_triggers = ['always','never','every','all','हमेशा','कभी नहीं','सभी']
        for atom in self.memory.graph.values():
            text = atom.to_text().lower()
            if any(t in text for t in rule_triggers):
                rule_atom = KnowledgeAtom(
                    atom_type  = AtomType.RULE,
                    content    = {'condition': text, 'conclusion': 'derived rule',
                                  'source_text': text},
                    confidence = 0.85, category = 'world_rule'
                )
                if self.memory.add_atom(rule_atom):
                    rules_found.append(f'Rule found: {text[:80]}')
        return rules_found

    def simulate_what_if(self, scenario: str) -> str:
        rules = [(a, a.content.get('condition',''))
                 for a in self.memory.graph.values()
                 if a.atom_type == AtomType.RULE]
        causal = [a for a in self.memory.graph.values()
                  if a.atom_type == AtomType.CAUSAL]

        if not rules and not causal:
            return 'Simulation failed: insufficient rules in knowledge base.'

        # Find applicable rules
        sw = set(scenario.lower().split())
        applicable = []
        for atom, cond in rules:
            cw = set(cond.lower().split())
            if len(sw & cw) >= 2:
                applicable.append(atom.content.get('conclusion', cond))

        for atom in causal:
            cause = atom.content.get('cause', '')
            cw = set(cause.lower().split())
            if len(sw & cw) >= 2:
                effect = atom.content.get('effect', '')
                applicable.append(f'This could cause: {effect}')

        if not applicable:
            return (f'Scenario [{scenario}]: No matching rules found. '
                    f'Train on domain data for better simulation.')

        results = ' | '.join(applicable[:3])
        return f'Simulation for [{scenario}]: {results}'
