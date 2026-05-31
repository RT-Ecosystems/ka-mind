# KA-Mind Neocortex — Advanced Reasoning Engine
# BUG FIXED: Language-agnostic (Hindi + English + others)
# BUG FIXED: Contradiction detection improved
import re
from .knowledge_atom import AtomType


class Neocortex:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def think_and_reason(self) -> list:
        thoughts = []
        facts = list(self.memory.graph.values())
        new_count = 0

        for atom1 in facts:
            if atom1.atom_type != AtomType.FACT: continue
            text1 = atom1.to_text().lower()

            for atom2 in facts:
                if atom2.atom_type != AtomType.FACT: continue
                if atom1.atom_id == atom2.atom_id: continue
                text2 = atom2.to_text().lower()

                # Language-agnostic: find shared subject
                words1 = set(text1.split())
                words2 = set(text2.split())
                shared = words1 & words2

                if len(shared) >= 2 and new_count < 50:
                    new_fact = f'{text1} AND {text2} -> combined insight'
                    thoughts.append(f'Reasoning: {text1} + {text2}')
                    new_count += 1

        return thoughts[:20]

    def detect_contradictions(self) -> list:
        alerts = []
        facts  = list(self.memory.graph.values())
        negation_words = ['not', 'no', 'never', 'false', 'incorrect',
                          'नहीं', 'न', 'गलत', 'असत्य', 'कभी नहीं']

        for i, atom1 in enumerate(facts):
            for atom2 in facts[i+1:]:
                t1 = atom1.to_text().lower()
                t2 = atom2.to_text().lower()

                # Check 1: Direct negation
                for neg in negation_words:
                    if (t1.replace(f' {neg}', '') == t2 or
                            t2.replace(f' {neg}', '') == t1):
                        atom1.confidence = max(0.0, atom1.confidence - 0.3)
                        atom2.confidence = max(0.0, atom2.confidence - 0.3)
                        alerts.append(
                            f'CONTRADICTION: [{t1[:50]}] vs [{t2[:50]}]')

                # Check 2: Same subject, conflicting predicates
                s1 = atom1.content.get('subject', '')
                s2 = atom2.content.get('subject', '')
                p1 = atom1.content.get('predicate', '')
                p2 = atom2.content.get('predicate', '')
                o1 = atom1.content.get('object', '')
                o2 = atom2.content.get('object', '')
                if (s1 and s1 == s2 and p1 == p2 == 'is'
                        and o1 and o2 and o1 != o2):
                    alerts.append(
                        f'CONFLICT: {s1} is [{o1}] vs [{o2}]')
        return alerts

    def run_deep_sleep_cycle(self):
        print('Neocortex Deep Sleep: analyzing graph...')
        alerts   = self.detect_contradictions()
        thoughts = self.think_and_reason()
        for a in alerts:   print(f'  ALERT: {a}')
        for t in thoughts: print(f'  THOUGHT: {t}')
        print(f'Done. Contradictions: {len(alerts)}, Insights: {len(thoughts)}')
