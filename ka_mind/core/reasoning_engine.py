# KA-Mind Reasoning Engine v2.3.1
# HOTFIX: Lower modus ponens threshold 0.6 -> 0.4
# HOTFIX: Causal chain now works with fixed CausalMapper
from .knowledge_atom import AtomType


class ReasoningEngine:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    # ── Modus Ponens: P + (P→Q) = Q ─────────────────────────
    def modus_ponens(self, query: str) -> list:
        results = []
        qw = set(query.lower().split())
        rules = [a for a in self.memory.graph.values()
                 if a.atom_type == AtomType.RULE
                 and a.content.get('category') != 'ethics']
        facts = [a for a in self.memory.graph.values()
                 if a.atom_type == AtomType.FACT]

        for rule in rules:
            cond = rule.content.get('condition', '')
            conc = rule.content.get('conclusion', '')
            if not cond or not conc: continue
            cw = set(cond.lower().split())

            # HOTFIX: lowered from 0.6 to 0.4
            query_match = len(qw & cw) / max(len(cw), 1)
            if query_match >= 0.4:
                # Find supporting fact
                best_fact = None
                best_score = 0.0
                for fact in facts:
                    fw = set(fact.to_text().lower().split())
                    score = len(cw & fw) / max(len(cw), 1)
                    if score > best_score:
                        best_score = score
                        best_fact  = fact
                if best_fact and best_score >= 0.35:
                    results.append({
                        'reasoning':   f'Premise: {best_fact.to_text()}',
                        'rule':        f'Rule: if {cond} then {conc}',
                        'conclusion':  f'Therefore: {conc}',
                        'confidence':  rule.confidence * best_fact.confidence
                    })
        return results[:3]

    # ── Forward Chaining ─────────────────────────────────────
    def forward_chain(self, max_steps: int = 5) -> list:
        derived = []
        rules = [a for a in self.memory.graph.values()
                 if a.atom_type == AtomType.RULE
                 and a.content.get('category') != 'ethics']
        known = {a.to_text().lower()
                 for a in self.memory.graph.values()
                 if a.atom_type in (AtomType.FACT, AtomType.RULE)}

        for step in range(max_steps):
            new_facts = []
            for rule in rules:
                cond = rule.content.get('condition', '').lower()
                conc = rule.content.get('conclusion', '').lower()
                if not cond or not conc or conc in known: continue
                cw = set(cond.split())
                for fact_text in list(known):
                    fw = set(fact_text.split())
                    if len(cw & fw) / max(len(cw), 1) >= 0.5:
                        new_facts.append(conc)
                        derived.append(
                            f'[Step {step+1}] {fact_text[:40]} + rule => {conc}')
                        break
            if not new_facts: break
            known.update(new_facts)
        return derived

    # ── Causal Chain ─────────────────────────────────────────
    def causal_chain(self, start: str, depth: int = 5) -> list:
        chain   = [start]
        current = start.lower()
        visited = set()
        causal  = [a for a in self.memory.graph.values()
                   if a.atom_type == AtomType.CAUSAL]

        for _ in range(depth):
            best_match = None
            best_score = 0.0
            for atom in causal:
                cause  = atom.content.get('cause', '').lower()
                effect = atom.content.get('effect', '').lower()
                if cause in visited: continue
                cw   = set(cause.split())
                curw = set(current.split())
                score = len(cw & curw) / max(len(cw), 1)
                if score > best_score:
                    best_score = best_match, best_match = (cause, effect), None
                    best_score, best_match = score, (cause, effect)
            if best_match and best_score >= 0.4:
                cause, effect = best_match
                chain.append(f'  -> {effect}')
                visited.add(cause)
                current = effect
            else:
                break
        return chain

    # ── Abductive Reasoning ──────────────────────────────────
    def abduction(self, observation: str) -> list:
        ow = set(observation.lower().split())
        explanations = []
        for atom in self.memory.graph.values():
            if atom.atom_type == AtomType.RULE:
                conc = atom.content.get('conclusion','').lower()
                cw   = set(conc.split())
                if len(ow & cw) / max(len(cw), 1) >= 0.4:
                    cond = atom.content.get('condition','')
                    explanations.append(f'Possible cause: {cond} (leads to: {conc})')
            elif atom.atom_type == AtomType.CAUSAL:
                effect = atom.content.get('effect','').lower()
                ew     = set(effect.split())
                if len(ow & ew) / max(len(ew), 1) >= 0.4:
                    cause = atom.content.get('cause','')
                    explanations.append(f'Best explanation: {cause}')
        return explanations[:4]

    # ── Deductive Syllogism ──────────────────────────────────
    def deductive_syllogism(self, query: str) -> list:
        results = []
        qw    = set(query.lower().split())
        facts = list(self.memory.graph.values())
        univ  = [a for a in facts
                 if a.atom_type == AtomType.FACT
                 and any(w in a.to_text().lower()
                         for w in ['all','every','always'])]
        spec  = [a for a in facts
                 if a.atom_type == AtomType.FACT and a not in univ]
        for u in univ:
            subj = u.content.get('subject','')
            obj  = u.content.get('object','')
            if not subj or not obj: continue
            for s in spec:
                s_subj = s.content.get('subject','')
                s_obj  = s.content.get('object','')
                if subj.lower() in s_obj.lower() and s_subj:
                    conclusion = f'{s_subj} is {obj}'
                    if len(qw & set(conclusion.split())) > 0:
                        results.append({'major': u.to_text(),
                                        'minor': s.to_text(),
                                        'conclusion': conclusion})
        return results[:3]

    # ── Main: pick best strategy ─────────────────────────────
    def reason(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ['why','because','explain','reason','क्यों']):
            r = self.abduction(query)
            if r: return ' | '.join(r[:2])
        mp = self.modus_ponens(query)
        if mp:
            b = mp[0]
            return (f"{b['reasoning']}. {b['rule']}. "
                    f"{b['conclusion']} ({b['confidence']:.0%})")
        syl = self.deductive_syllogism(query)
        if syl:
            return (f"{syl[0]['major']} + {syl[0]['minor']} "
                    f"=> {syl[0]['conclusion']}")
        chain = self.causal_chain(query)
        if len(chain) > 1:
            return ' '.join(chain)
        return ''
