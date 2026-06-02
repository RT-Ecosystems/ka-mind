"""
SuperTeacher v1.0 — Complete training script for NeuraBrain agents.
Teaches: Reasoning, Imagination, Ethics, Web Search, Code, Languages, Novel Writing.
No guesswork. No millions of iterations. One pass, permanent learning.
"""
from ka_mind.core.fact_extractor   import FactExtractor
from ka_mind.core.rule_extractor   import RuleExtractor
from ka_mind.core.causal_mapper    import CausalMapper
from ka_mind.core.knowledge_atom   import KnowledgeAtom, AtomType
from ka_mind.core.language_rules   import LanguageRules, LangRule


class SuperTeacher:
    """Master trainer that teaches an agent EVERYTHING through explicit rules."""

    def __init__(self, graph_memory, vector_graph=None):
        self.memory          = graph_memory
        self.vector_graph    = vector_graph
        self.fact_extractor  = FactExtractor()
        self.rule_extractor  = RuleExtractor()
        self.causal_mapper   = CausalMapper()
        self.lang_rules      = LanguageRules()
        self._chunks         = 0
        self._atoms_created  = 0
        self._teach_foundations()

    # ── Step 0: Teach the absolute basics ───────────────
    def _teach_foundations(self):
        """Teach fundamental knowledge that every agent MUST know."""
        foundations = [
            # Logical foundations
            KnowledgeAtom(AtomType.RULE,
                {"condition": "something is true", "conclusion": "it cannot be false at the same time"},
                1.0, category="logic"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "A equals B", "conclusion": "B equals A"},
                1.0, category="logic"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "A causes B and B causes C",
                 "conclusion": "A can cause C indirectly"},
                0.95, category="logic"),
            # Reasoning foundations
            KnowledgeAtom(AtomType.FACT,
                {"text": "Reasoning means connecting facts to reach new conclusions.",
                 "subject": "reasoning", "predicate": "means",
                 "object": "connecting facts to reach new conclusions"},
                1.0, category="meta"),
            KnowledgeAtom(AtomType.FACT,
                {"text": "Imagination means combining known things in new ways.",
                 "subject": "imagination", "predicate": "means",
                 "object": "combining known things in new ways"},
                1.0, category="meta"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "you need to imagine something new",
                 "conclusion": "combine existing knowledge atoms in novel ways"},
                0.9, category="meta"),
            # Language foundations
            KnowledgeAtom(AtomType.FACT,
                {"text": "Different languages have different word orders. "
                 "Hindi uses SOV (Subject-Object-Verb). English uses SVO (Subject-Verb-Object).",
                 "subject": "language", "predicate": "varies",
                 "object": "word order"},
                1.0, category="language"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "user asks in a specific language",
                 "conclusion": "respond in the same language with proper grammar"},
                1.0, category="language"),
            # Ethics foundations
            KnowledgeAtom(AtomType.RULE,
                {"condition": "user asks harmful content",
                 "conclusion": "refuse and explain why it is harmful"},
                1.0, category="ethics"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "information is uncertain",
                 "conclusion": "say 'I am not sure' instead of guessing"},
                1.0, category="ethics"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "user needs help urgently",
                 "conclusion": "prioritize safety and provide immediate helpful response"},
                1.0, category="ethics"),
            # Novel writing foundations
            KnowledgeAtom(AtomType.FACT,
                {"text": "A good story has a beginning (introduction), "
                 "middle (conflict/events), and end (resolution).",
                 "subject": "story", "predicate": "has",
                 "object": "beginning, middle, and end"},
                1.0, category="writing"),
            KnowledgeAtom(AtomType.RULE,
                {"condition": "writing a story or novel",
                 "conclusion": "create characters, setting, conflict, and resolution"},
                0.95, category="writing"),
        ]
        for atom in foundations:
            self.memory.add_atom(atom)

    # ── Main training method ───────────────────────────
    def teach(self, text: str, domain: str = "general",
              user_id: str = "system") -> int:
        """Process text through ALL teaching layers in one pass."""
        before = len(self.memory.graph)

        # Layer 1: Facts (WHAT)
        for atom in self.fact_extractor.extract(text, domain, user_id):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)

        # Layer 2: Rules (HOW)
        for atom in self.rule_extractor.extract(text, domain, user_id):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)

        # Layer 3: Causality (WHY)
        for atom in self.causal_mapper.extract(text, domain, user_id):
            if self.memory.add_atom(atom):
                self._add_to_vector(atom)

        # Layer 4: Build connections
        self._build_edges()

        self._chunks += 1
        created = len(self.memory.graph) - before
        self._atoms_created += created
        return created

    def teach_language(self, lang_code: str, lang_rule: LangRule,
                       sample_texts: list) -> int:
        """Teach a new language to the agent by providing grammar rules and samples."""
        total = 0

        # Add language rule
        LanguageRules.add_language(lang_code, lang_rule)

        # Teach grammar as knowledge atoms
        grammar_atom = KnowledgeAtom(AtomType.FACT,
            {"text": f"{lang_rule.name} uses {lang_rule.word_order} word order.",
             "subject": lang_rule.name, "predicate": "uses",
             "object": f"{lang_rule.word_order} word order"},
            1.0, category="language")
        self.memory.add_atom(grammar_atom)
        total += 1

        # Teach sample texts
        for text in sample_texts:
            total += self.teach(text, domain="language")

        return total

    def teach_agent(self, agent_name: str,
                    capabilities: list,
                    instructions: list) -> int:
        """Teach an agent how to use its capabilities."""
        total = 0

        # Register agent capabilities
        for cap in capabilities:
            atom = KnowledgeAtom(AtomType.FACT,
                {"text": f"{agent_name} can {cap}.",
                 "subject": agent_name, "predicate": "can", "object": cap},
                1.0, category="agent")
            self.memory.add_atom(atom)
            total += 1

        # Register agent instructions
        for instr in instructions:
            atom = KnowledgeAtom(AtomType.RULE,
                {"condition": f"{agent_name} receives task related to {instr['trigger']}",
                 "conclusion": instr['action']},
                0.95, category="agent")
            self.memory.add_atom(atom)
            total += 1

        return total

    def _add_to_vector(self, atom):
        if self.vector_graph is None: return
        try:
            from ka_mind.core.vector_atom import VectorAtom
            va = VectorAtom(atom.to_text(), atom.category)
            self.vector_graph.add_atom(va)
        except Exception: pass

    def _build_edges(self):
        atoms = list(self.memory.graph.values())[-30:]
        for i, a1 in enumerate(atoms):
            for a2 in atoms[i+1:]:
                t1 = set(a1.to_text().lower().split())
                t2 = set(a2.to_text().lower().split())
                overlap = len(t1 & t2) / max(len(t1 | t2), 1)
                if overlap > 0.35:
                    self.memory.add_edge(a1.atom_id, a2.atom_id, "related", overlap)

    @property
    def stats(self):
        return {"chunks": self._chunks, "atoms": self._atoms_created,
                "total": len(self.memory.graph)}
