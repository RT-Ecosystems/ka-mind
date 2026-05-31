# NeuraBrain Human Language Engine
# Converts Knowledge Atoms -> Natural Human-like Text
# Goal: No one should know NeuraBrain wrote it
import random
from .knowledge_atom import AtomType


class HumanLanguageEngine:

    # Sentence openers — variety prevents robotic feel
    OPENERS = [
        '', '', '',  # Often no opener (most natural)
        'In essence, ', 'Simply put, ', 'To be precise, ',
        'Interestingly, ', 'Notably, ', 'As it turns out, ',
        'It is worth knowing that ', 'One must understand that ',
    ]

    # Connectors between sentences
    CONNECTORS = {
        'addition':  ['Moreover, ','Furthermore, ','Additionally, ',
                      'On top of this, ','What is more, ','Also, '],
        'contrast':  ['However, ','Nevertheless, ','That said, ',
                      'On the other hand, ','Yet, ','Even so, '],
        'cause':     ['As a result, ','Consequently, ','Therefore, ',
                      'This means that ','Hence, ','Thus, '],
        'example':   ['For instance, ','To illustrate, ',
                      'For example, ','Specifically, '],
        'emphasis':  ['Indeed, ','In fact, ','Notably, ',
                      'It is important to note that '],
        'time':      ['Over time, ','Historically, ','In recent times, ',
                      'Throughout history, '],
    }

    # Fact sentence templates — vary structure
    FACT_TEMPLATES = [
        '{subject} is {predicate} {object}.',
        '{subject}, often described as {object}, plays a vital role.',
        'What we know as {subject} is fundamentally {object}.',
        'The concept of {subject} refers to {object}.',
        '{subject} can be defined as {object}.',
        'At its core, {subject} represents {object}.',
        'Known for being {object}, {subject} stands out remarkably.',
    ]

    CAUSAL_TEMPLATES = [
        '{cause}, which directly leads to {effect}.',
        'When {cause}, the natural outcome is {effect}.',
        '{cause}. As a direct consequence, {effect}.',
        'The relationship between {cause} and {effect} is well established.',
        '{cause} — and this is where {effect} becomes apparent.',
        'Because {cause}, we observe that {effect}.',
    ]

    RULE_TEMPLATES = [
        'It holds true that when {condition}, {conclusion}.',
        'A fundamental principle: {condition} invariably leads to {conclusion}.',
        'Experience shows that {condition}, and therefore {conclusion}.',
        'Whenever {condition}, one can expect {conclusion}.',
        '{condition} — from this, {conclusion} follows naturally.',
    ]

    CONCEPT_TEMPLATES = [
        '{name} is best understood as {definition}.',
        'The term {name} encompasses {definition}.',
        '{name}, in its truest sense, means {definition}.',
        'When we speak of {name}, we refer to {definition}.',
    ]

    # Closing sentences — give a human 'finishing touch'
    CLOSINGS = [
        '',  # Often no closing
        ' This understanding forms the foundation of the subject.',
        ' These principles work together in remarkable ways.',
        ' Such nuances make this topic particularly fascinating.',
        ' Understanding this deeply changes how one sees the world.',
        ' The implications of this extend further than most realize.',
    ]

    # Question-type detection for response style
    WHAT_WORDS  = ['what','क्या','कौन','who','which','कौनसा']
    WHY_WORDS   = ['why','क्यों','reason','कारण']
    HOW_WORDS   = ['how','कैसे','manner','तरीका']
    TELL_WORDS  = ['tell','explain','describe','बताओ','समझाओ','बताइए']
    WRITE_WORDS = ['write','लिखो','story','novel','article','essay',
                   'poem','कविता','कहानी','लेख']

    def __init__(self):
        random.seed()

    def generate(self, query: str, atoms: list,
                 style: str = 'auto') -> str:
        if not atoms:
            return self._no_knowledge_response(query)

        if style == 'auto':
            style = self._detect_style(query)

        if style == 'creative':
            return self._creative_response(query, atoms)
        elif style == 'conversational':
            return self._conversational_response(query, atoms)
        else:
            return self._factual_response(query, atoms)

    # ── Style detection ──────────────────────────────────────
    def _detect_style(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in self.WRITE_WORDS):
            return 'creative'
        if len(query.split()) <= 6:
            return 'conversational'
        return 'factual'

    # ── Factual response (encyclopaedia style) ───────────────
    def _factual_response(self, query: str, atoms: list) -> str:
        from .knowledge_atom import AtomType
        facts    = [a for a in atoms if a.atom_type == AtomType.FACT]
        concepts = [a for a in atoms if a.atom_type == AtomType.CONCEPT]
        causal   = [a for a in atoms if a.atom_type == AtomType.CAUSAL]
        rules    = [a for a in atoms if a.atom_type == AtomType.RULE]

        sentences = []

        # Start with concept definition if available
        for a in concepts[:1]:
            sentences.append(self._render_concept(a))

        # Core facts
        for i, a in enumerate(facts[:3]):
            sent = self._render_fact(a)
            if i > 0 and sentences:
                sent = random.choice(self.CONNECTORS['addition']) + sent
            sentences.append(sent)

        # Causal relationships
        for i, a in enumerate(causal[:2]):
            sent = self._render_causal(a)
            if sentences:
                sent = random.choice(self.CONNECTORS['cause']) + sent
            sentences.append(sent)

        # Rules as conclusions
        for a in rules[:1]:
            sent = self._render_rule(a)
            if sentences:
                sent = random.choice(self.CONNECTORS['emphasis']) + sent
            sentences.append(sent)

        # Optional closing
        closing = random.choice(self.CLOSINGS)
        if closing and sentences:
            sentences[-1] = sentences[-1].rstrip('.') + closing

        return self._format_paragraph(sentences)

    # ── Conversational response (short, friendly) ────────────
    def _conversational_response(self, query: str,
                                 atoms: list) -> str:
        from .knowledge_atom import AtomType
        q = query.lower()

        if any(w in q for w in self.WHAT_WORDS):
            prefix = ''
        elif any(w in q for w in self.WHY_WORDS):
            prefix = 'The reason is: '
        elif any(w in q for w in self.HOW_WORDS):
            prefix = 'Here is how: '
        else:
            prefix = ''

        best = atoms[0]
        core = self._atom_to_sentence(best)

        extras = []
        for a in atoms[1:3]:
            extras.append(self._atom_to_sentence(a))

        result = prefix + core
        if extras:
            conn = random.choice(self.CONNECTORS['addition'])
            result += ' ' + conn + extras[0].lower()
        return result.strip()

    # ── Creative response (story/novel/article style) ─────────
    def _creative_response(self, query: str, atoms: list) -> str:
        # Extract topic from query
        topic = self._extract_topic(query)

        # Build narrative from atoms
        all_texts = [self._atom_to_sentence(a) for a in atoms[:8]]

        # Narrative structure: Hook → Body → Insight → Close
        hook    = self._craft_hook(topic, all_texts)
        body    = self._craft_body(all_texts[1:])
        insight = self._craft_insight(atoms)
        close   = self._craft_close(topic)

        return f'{hook}\n\n{body}\n\n{insight}\n\n{close}'

    def _craft_hook(self, topic: str, texts: list) -> str:
        hooks = [
            f'There is something quietly extraordinary about {topic}.',
            f'Few things in life are as layered as {topic}.',
            f'To truly understand {topic}, one must first appreciate its depth.',
            f'{topic} has always carried a certain weight — one that demands attention.',
            f'The story of {topic} is not a simple one.',
        ]
        opening = random.choice(hooks)
        if texts:
            opening += ' ' + texts[0]
        return opening

    def _craft_body(self, texts: list) -> str:
        if not texts: return ''
        parts = []
        connectors = ([''] + self.CONNECTORS['addition'] +
                      self.CONNECTORS['contrast'] +
                      self.CONNECTORS['cause'])
        for i, text in enumerate(texts[:4]):
            conn = random.choice(connectors) if i > 0 else ''
            parts.append(conn + text)
        return ' '.join(parts)

    def _craft_insight(self, atoms: list) -> str:
        causal = [a for a in atoms if a.atom_type == AtomType.CAUSAL]
        rules  = [a for a in atoms if a.atom_type == AtomType.RULE]
        if causal:
            return random.choice(self.CONNECTORS['emphasis']) + self._render_causal(causal[0])
        if rules:
            return random.choice(self.CONNECTORS['emphasis']) + self._render_rule(rules[0])
        return ''

    def _craft_close(self, topic: str) -> str:
        closes = [
            f'And perhaps that is what makes {topic} so endlessly worth exploring.',
            f'Such is the nature of {topic} — complex, layered, and deeply human.',
            f'The more one looks into {topic}, the more one finds there is still to understand.',
            f'{topic}, in the end, reveals as much about us as it does about itself.',
        ]
        return random.choice(closes)

    # ── Atom renderers ────────────────────────────────────────
    def _render_fact(self, atom) -> str:
        c    = atom.content
        subj = c.get('subject', '').strip()
        pred = c.get('predicate', 'is').strip()
        obj  = c.get('object', '').strip()
        text = c.get('text', '').strip()

        if subj and obj:
            tmpl = random.choice(self.FACT_TEMPLATES)
            return tmpl.format(subject=subj, predicate=pred, object=obj)
        if text:
            return self._polish(text)
        return atom.to_text()

    def _render_causal(self, atom) -> str:
        c      = atom.content
        cause  = c.get('cause', '').strip()
        effect = c.get('effect', '').strip()
        if cause and effect:
            tmpl = random.choice(self.CAUSAL_TEMPLATES)
            return tmpl.format(cause=cause, effect=effect)
        return atom.to_text()

    def _render_rule(self, atom) -> str:
        c    = atom.content
        cond = c.get('condition', '').strip()
        conc = c.get('conclusion', '').strip()
        if cond and conc:
            tmpl = random.choice(self.RULE_TEMPLATES)
            return tmpl.format(condition=cond, conclusion=conc)
        return atom.to_text()

    def _render_concept(self, atom) -> str:
        c    = atom.content
        name = c.get('name', '').strip()
        defn = c.get('definition', c.get('description', '')).strip()
        if name and defn:
            tmpl = random.choice(self.CONCEPT_TEMPLATES)
            return tmpl.format(name=name, definition=defn)
        return atom.to_text()

    def _atom_to_sentence(self, atom) -> str:
        t = atom.atom_type
        if t == AtomType.FACT:    return self._render_fact(atom)
        if t == AtomType.CAUSAL:  return self._render_causal(atom)
        if t == AtomType.RULE:    return self._render_rule(atom)
        if t == AtomType.CONCEPT: return self._render_concept(atom)
        return self._polish(atom.to_text())

    # ── Utilities ─────────────────────────────────────────────
    def _polish(self, text: str) -> str:
        if not text: return text
        text = text.strip()
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        if text and text[-1] not in '.!?':
            text += '.'
        return text

    def _format_paragraph(self, sentences: list) -> str:
        cleaned = [self._polish(s) for s in sentences if s and s.strip()]
        if not cleaned: return ''
        return ' '.join(cleaned)

    def _extract_topic(self, query: str) -> str:
        stop = {'write','a','an','the','about','on','for','me',
                'लिखो','एक','के','बारे','में','पर'}
        words = [w for w in query.lower().split() if w not in stop]
        return ' '.join(words[:3]) if words else query

    def _no_knowledge_response(self, query: str) -> str:
        responses = [
            'I do not have sufficient knowledge on this yet. Train me with relevant data.',
            'This topic is outside my current knowledge base. Add training data to help me learn.',
            'I am still learning about this. Provide training data and I will grow wiser.',
        ]
        return random.choice(responses)
