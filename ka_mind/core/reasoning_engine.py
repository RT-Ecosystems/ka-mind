# KA-Mind Reasoning Engine v2.3
# Real formal logic — modus ponens, deduction, abduction
# Replaces the useless 'combined insight' approach
from .knowledge_atom import AtomType


class ReasoningEngine:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    # ── Forward Chaining: Given facts, derive new conclusions ─
    def forward_chain(self, max_steps: int = 5) -> list:
        derived = []
        rules = [a for a in self.memory.graph.values()
                 if a.atom_type == AtomType.RULE]
        facts = {a.to_text().lower(): a
                 for a in self.memory.graph.values()
                 if a.atom_type == AtomType.FACT}

        for step in range(max_steps):
            new_facts = []
            for rule in rules:
                cond = rule.content.get('condition', '')
                conc = rule.content.get('conclusion', '')
                if not cond or not conc: continue
                cond_words = set(cond.lower().split())
                for fact_text, fact_atom in facts.items():
                    fact_words = set(fact_text.split())
                    overlap = len(cond_words & fact_words)
                    coverage = overlap / max(len(cond_words), 1)
                    if coverage >= 0.6:
                        new_conclusion = conc
                        if new_conclusion not in facts:
                            new_facts.append({
                                'conclusion': new_conclusion,
                                'from_fact': fact_text,
                                'by_rule': cond + ' -> ' + conc,
                                'confidence': rule.confidence * fact_atom.confidence
                            })
                            derived.append(
                                f'[Step {step+1}] {fact_text} + rule({cond}) => {new_conclusion}'
                            )
            for nf in new_facts:
                facts[nf['conclusion']] = type('Atom', (), {
                    'to_text': lambda self, t=nf['conclusion']: t,
                    'confidence': nf['confidence'],
                    'atom_type': AtomType.FACT
                })()
            if not new_facts: break
        return derived

    # ── Modus Ponens: P, P→Q therefore Q ─────────────────────
    def modus_ponens(self, query: str) -> list:
        results = []
        qw = set(query.lower().split())
        rules = [a for a in self.memory.graph.values()
                 if a.atom_type == AtomType.RULE]
        facts = [a for a in self.memory.graph.values()
                 if a.atom_type == AtomType.FACT]

        for rule in rules:
            cond = rule.content.get('condition', '')
            conc = rule.content.get('conclusion', '')
            cw   = set(cond.lower().split())

            # Does query match the condition?
            if len(qw & cw) / max(len(cw), 1) >= 0.5:
                # Verify at least one supporting fact exists
                for fact in facts:
                    fw = set(fact.to_text().lower().split())
                    if len(cw & fw) / max(len(cw), 1) >= 0.5:
                        results.append({
                            'reasoning': f'Premise: {fact.to_text()}',
                            'rule':      f'Rule: If {cond} then {conc}',
                            'conclusion': f'Therefore: {conc}',
                            'confidence': rule.confidence * fact.confidence
                        })
                        break
        return results[:3]

    # ── Deductive Syllogism: All A are B, X is A → X is B ────
    def deductive_syllogism(self, query: str) -> list:
        results = []
        qw    = set(query.lower().split())
        facts = list(self.memory.graph.values())

        universal = [a for a in facts
                     if a.atom_type == AtomType.FACT
                     and any(w in a.to_text().lower()
                             for w in ['all','every','always','सभी','हर'])]

        specific  = [a for a in facts
                     if a.atom_type == AtomType.FACT
                     and a not in universal]

        for univ in universal:
            uw = set(univ.to_text().lower().split())
            subj = univ.content.get('subject', '')
            obj  = univ.content.get('object', '')
            if not subj or not obj: continue

            for spec in specific:
                spec_text = spec.to_text().lower()
                spec_subj = spec.content.get('subject', '')
                spec_obj  = spec.content.get('object', '')

                # X is A (specific fact) + All A are B → X is B
                if subj.lower() in spec_obj.lower():
                    conclusion = f'{spec_subj} is {obj}'
                    if len(qw & set(conclusion.split())) > 0:
                        results.append({
                            'type': 'syllogism',
                            'major': univ.to_text(),
                            'minor': spec.to_text(),
                            'conclusion': conclusion
                        })
        return results[:3]

    # ── Causal Chain: A causes B, B causes C → A causes C ────
    def causal_chain(self, start: str, depth: int = 4) -> list:
        chain   = [start]
        current = start.lower()
        causal  = [a for a in self.memory.graph.values()
                   if a.atom_type == AtomType.CAUSAL]

        for _ in range(depth):
            found = False
            for atom in causal:
                cause  = atom.content.get('cause', '').lower()
                effect = atom.content.get('effect', '').lower()
                cw = set(cause.split())
                curw = set(current.split())
                if len(cw & curw) / max(len(cw), 1) >= 0.5:
                    chain.append(f'  -> {effect} (causes it)')
                    current = effect
                    found = True
                    break
            if not found: break
        return chain

    # ── Abductive Reasoning: Best explanation for observation ─
    def abduction(self, observation: str) -> list:
        ow      = set(observation.lower().split())
        rules   = [a for a in self.memory.graph.values()
                   if a.atom_type == AtomType.RULE]
        causal  = [a for a in self.memory.graph.values()
                   if a.atom_type == AtomType.CAUSAL]
        explanations = []

        # Find rules where conclusion matches observation
        for rule in rules:
            conc = rule.content.get('conclusion','').lower()
            cw   = set(conc.split())
            if len(ow & cw) / max(len(cw), 1) >= 0.5:
                cond = rule.content.get('condition','')
                explanations.append(f'Possible cause: {cond} (leads to: {conc})')

        # Find causal atoms where effect matches
        for atom in causal:
            effect = atom.content.get('effect','').lower()
            ew     = set(effect.split())
            if len(ow & ew) / max(len(ew), 1) >= 0.5:
                cause = atom.content.get('cause','')
                explanations.append(f'Best explanation: {cause}')

        return explanations[:3]

    # ── Main entry: pick best reasoning strategy ──────────────
    def reason(self, query: str) -> str:
        query_lower = query.lower()

        # Why/because/explain → abduction
        if any(w in query_lower for w in ['why','because','explain','reason','क्यों']):
            results = self.abduction(query)
            if results: return ' | '.join(results)

        # Modus ponens first
        mp = self.modus_ponens(query)
        if mp:
            best = mp[0]
            return (f"{best['reasoning']}. {best['rule']}. {best['conclusion']}"
                    f" (confidence: {best['confidence']:.0%})")

        # Syllogism
        syl = self.deductive_syllogism(query)
        if syl:
            return (f"{syl[0]['major']} + {syl[0]['minor']} => {syl[0]['conclusion']}")

        # Causal chain
        chain = self.causal_chain(query)
        if len(chain) > 1:
            return ' '.join(chain)

        return ''
