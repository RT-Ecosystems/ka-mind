"""
FluidComposer v1.0 — Template-free Natural Language Generation
No fixed templates. Uses grammar rules + Knowledge Atoms to compose unique sentences every time.
"""
import random
from .knowledge_atom import AtomType


class FluidComposer:
    """Generates human-like text WITHOUT fixed templates."""

    # Grammar connectors
    SUBJECTS_HI = ["यह", "वह", "इसका", "उसका", "हम", "आप"]
    SUBJECTS_EN = ["It", "This", "That", "Which", "The concept"]

    VERBS_IS_HI  = ["है", "होता है", "माना जाता है", "कहलाता है", "हुआ करता है"]
    VERBS_IS_EN  = ["is", "refers to", "can be defined as", "represents", "means"]

    VERBS_CAUSE_HI = ["की वजह से", "के कारण", "की वजह से ही", "के चलते"]
    VERBS_CAUSE_EN = ["because of", "due to", "as a result of", "owing to"]

    VERBS_RULE_HI = ["तो", "हमेशा", "ज़रूर", "निश्चित रूप से"]
    VERBS_RULE_EN = ["then", "always", "certainly", "invariably"]

    CONNECTORS_HI = ["और", "इसके अलावा", "साथ ही", "यही नहीं, बल्कि"]
    CONNECTORS_EN = ["and", "moreover", "furthermore", "in addition"]

    def __init__(self, graph_memory, reasoning_engine=None):
        self.memory   = graph_memory
        self.reasoner = reasoning_engine

    def compose(self, query: str, relevant_atoms: list, style: str = 'auto') -> str:
        """Main entry point — generates a complete response without templates."""
        if not relevant_atoms:
            # Try reasoning
            if self.reasoner:
                reasoned = self.reasoner.reason(query)
                if reasoned:
                    return reasoned
            return f"मुझे इस बारे में और जानकारी चाहिए: {query}"

        lang = self._detect_language(query)
        sentences = []

        # Process facts
        facts = [a for a in relevant_atoms if a.atom_type == AtomType.FACT][:4]
        for i, atom in enumerate(facts):
            sent = self._compose_fact(atom, lang, is_first=(i == 0))
            sentences.append(sent)

        # Process rules
        rules = [a for a in relevant_atoms if a.atom_type == AtomType.RULE][:2]
        for atom in rules:
            sent = self._compose_rule(atom, lang)
            sentences.append(sent)

        # Process causal
        causal = [a for a in relevant_atoms if a.atom_type == AtomType.CAUSAL][:2]
        for atom in causal:
            sent = self._compose_causal(atom, lang)
            sentences.append(sent)

        # Add reasoning conclusion if available
        if self.reasoner:
            reasoned = self.reasoner.reason(query)
            if reasoned and reasoned not in " ".join(sentences):
                sentences.append(reasoned)

        return " ".join(sentences).strip() + "."

    def _detect_language(self, text: str) -> str:
        hindi_chars = sum(1 for c in text if 'ऀ' <= c <= 'ॿ')
        return 'hi' if hindi_chars > len(text) * 0.2 else 'en'

    def _compose_fact(self, atom, lang, is_first=False):
        c = atom.content
        subj = c.get('subject', c.get('text', ''))
        pred = c.get('predicate', 'is')
        obj  = c.get('object', c.get('text', ''))

        if lang == 'hi':
            verb = random.choice(self.VERBS_IS_HI)
            if is_first:
                return f"{subj} {obj} {verb}"
            connector = random.choice(self.CONNECTORS_HI)
            return f"{connector}, {subj} {obj} {verb}"
        else:
            verb = random.choice(self.VERBS_IS_EN)
            if is_first:
                return f"{subj} {verb} {obj}"
            connector = random.choice(self.CONNECTORS_EN)
            return f"{connector}, {subj} {verb} {obj}"

    def _compose_rule(self, atom, lang):
        c = atom.content
        cond = c.get('condition', '')
        conc = c.get('conclusion', '')

        if lang == 'hi':
            verb = random.choice(self.VERBS_RULE_HI)
            return f"जब {cond}, {verb} {conc}"
        else:
            verb = random.choice(self.VERBS_RULE_EN)
            return f"When {cond}, {verb} {conc}"

    def _compose_causal(self, atom, lang):
        c = atom.content
        cause  = c.get('cause', '')
        effect = c.get('effect', '')

        if lang == 'hi':
            verb = random.choice(self.VERBS_CAUSE_HI)
            return f"{cause} {verb} {effect} होता है"
        else:
            verb = random.choice(self.VERBS_CAUSE_EN)
            return f"{effect} happens {verb} {cause}"

    def generate_novel(self, prompt: str, atoms: list, length: int = 600) -> str:
        """Generate a full novel without templates — using grammar composition."""
        lang = self._detect_language(prompt)
        words = prompt.split()
        character = words[0] if words else "नायक"
        place = words[-1] if len(words) > 1 else "एक स्थान"

        sentences = []

        # Opening
        if lang == 'hi':
            sentences.append(f"यह कहानी {place} की है, जहाँ {character} रहता था।")
        else:
            sentences.append(f"This is the story of {place}, where {character} lived.")

        # Middle — use atoms as plot points
        for atom in atoms:
            if atom.atom_type == AtomType.FACT:
                sentences.append(self._compose_fact(atom, lang))
            elif atom.atom_type == AtomType.CAUSAL:
                sentences.append(self._compose_causal(atom, lang))

        # Fill to reach target length
        while len(" ".join(sentences).split()) < length:
            if atoms:
                atom = random.choice(atoms)
                if atom.atom_type == AtomType.FACT:
                    sentences.append(self._compose_fact(atom, lang))
                else:
                    break
            else:
                break

        # Ending
        if lang == 'hi':
            sentences.append(f"इस तरह {character} ने सीखा कि सच्चाई सबसे बड़ी ताकत है।")
        else:
            sentences.append(f"And so, {character} learned that truth is the greatest power.")

        return " ".join(sentences)
