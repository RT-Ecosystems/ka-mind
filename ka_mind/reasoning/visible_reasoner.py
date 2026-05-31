# KA-Mind Visible Reasoner — Transparent thinking
# BUG FIXED: retrieve_context now works (method added to GraphMemory)
import time
from typing import Tuple


class VisibleReasoner:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def think_and_answer(self, query: str,
                         start_atom_id: str = None) -> Tuple[str, str]:
        thoughts = [
            f'Thinking: {query}',
            f'Searching GraphMemory...',
        ]

        # Step 1: Keyword search
        keyword_results = self.memory.search_scored(query, top_k=10)

        # Step 2: Graph context traversal (BUG FIXED)
        context_nodes = []
        if start_atom_id:
            context_nodes = self.memory.retrieve_context(start_atom_id, depth=2)
        elif keyword_results:
            best_atom = keyword_results[0][0]
            context_nodes = self.memory.retrieve_context(best_atom.atom_id, depth=2)

        if not keyword_results and not context_nodes:
            thoughts.append('No relevant atoms found.')
            return '\n'.join(thoughts), 'Insufficient knowledge for this query.'

        thoughts.append(f'Found {len(keyword_results)} keyword matches + '
                        f'{len(context_nodes)} graph context nodes.')

        facts   = []
        rules   = []
        causal  = []

        for atom, score in keyword_results:
            t = atom.atom_type.value
            txt = atom.to_text()
            thoughts.append(f'  [{t.upper()}|{score:.2f}] {txt[:80]}')
            if t == 'fact':   facts.append(txt)
            elif t == 'rule': rules.append(txt)
            elif t == 'causal': causal.append(txt)

        final = f'Query: {query}\n'
        if facts:  final += 'Facts: ' + ' | '.join(facts[:3]) + '.\n'
        if rules:  final += 'Rules: ' + ' | '.join(rules[:2]) + '.\n'
        if causal: final += 'Causality: ' + ' | '.join(causal[:2]) + '.\n'

        return '\n'.join(thoughts), final.strip()
