# NeuraBrain Human Language Engine v3.0
# Enhanced with 15+ FACT_TEMPLATES, 10 CAUSAL, 10 RULE, Novel Writing
# Goal: No one should know NeuraBrain wrote it
import random
from .knowledge_atom import AtomType


class HumanLanguageEngine:

    # ── Sentence openers ─────────────────────────────────
    OPENERS = [
        '', '', '', '',  # No opener (most natural)
        'In essence, ', 'Simply put, ', 'To be precise, ',
        'Interestingly, ', 'Notably, ', 'As it turns out, ',
        'It is worth knowing that ', 'One must understand that ',
        'The truth is, ', 'Believe it or not, ',
        'Here is the thing: ', 'Let me put it this way: ',
    ]

    # ── Connectors ───────────────────────────────────────
    CONNECTORS = {
        'addition':  ['Moreover, ','Furthermore, ','Additionally, ',
                      'On top of this, ','What is more, ','Also, ',
                      'Beyond that, ','Plus, ','Adding to this, '],
        'contrast':  ['However, ','Nevertheless, ','That said, ',
                      'On the other hand, ','Yet, ','Even so, ',
                      'But then again, ','In contrast, '],
        'cause':     ['As a result, ','Consequently, ','Therefore, ',
                      'This means that ','Hence, ','Thus, ',
                      'Because of this, ','For this reason, '],
        'example':   ['For instance, ','To illustrate, ',
                      'For example, ','Specifically, ',
                      'A good example is, ','Consider this: '],
        'emphasis':  ['Indeed, ','In fact, ','Notably, ',
                      'It is important to note that ',
                      'Crucially, ','More importantly, '],
        'time':      ['Over time, ','Historically, ','In recent times, ',
                      'Throughout history, ','Lately, ',
                      'In the past few years, '],
    }

    # ── FACT TEMPLATES (15+ diverse) ─────────────────────
    FACT_TEMPLATES = [
        '{subject} is {predicate} {object}.',
        '{subject}, often described as {object}, plays a vital role.',
        'What we know as {subject} is fundamentally {object}.',
        'The concept of {subject} refers to {object}.',
        '{subject} can be defined as {object}.',
        'At its core, {subject} represents {object}.',
        'Known for being {object}, {subject} stands out remarkably.',
        '{subject} — this is essentially {object}.',
        'When you think of {subject}, what comes to mind is {object}.',
        '{subject} has always been understood as {object}.',
        'In simple words, {subject} means {object}.',
        '{subject} is nothing but {object}.',
        'People often say that {subject} is {object}.',
        'It is widely accepted that {subject} is {object}.',
        'Without a doubt, {subject} can be described as {object}.',
        '{subject} की सबसे अच्छी परिभाषा है — {object}.',
        '{subject} को हम {object} के रूप में जानते हैं।',
    ]

    # ── CAUSAL TEMPLATES (10 diverse) ────────────────────
    CAUSAL_TEMPLATES = [
        '{cause}, which directly leads to {effect}.',
        'When {cause}, the natural outcome is {effect}.',
        '{cause}. As a direct consequence, {effect}.',
        'The relationship between {cause} and {effect} is well established.',
        '{cause} — and this is where {effect} becomes apparent.',
        'Because {cause}, we observe that {effect}.',
        '{cause} की वजह से {effect} होता है।',
        '{cause} के कारण ही {effect} संभव हो पाता है।',
        'The reason we see {effect} is simply {cause}.',
        '{effect} happens precisely because {cause}.',
    ]

    # ── RULE TEMPLATES (10 diverse) ──────────────────────
    RULE_TEMPLATES = [
        'It holds true that when {condition}, {conclusion}.',
        'A fundamental principle: {condition} invariably leads to {conclusion}.',
        'Experience shows that {condition}, and therefore {conclusion}.',
        'Whenever {condition}, one can expect {conclusion}.',
        '{condition} — from this, {conclusion} follows naturally.',
        'The rule is simple: if {condition}, then {conclusion}.',
        '{condition} तो {conclusion} — यह एक सिद्धांत है।',
        'जब भी {condition}, तब {conclusion} ही होता है।',
        'It is a well-known fact that {condition} results in {conclusion}.',
        'Without exception, {condition} brings about {conclusion}.',
    ]

    # ── STORY TEMPLATES for generate_novel ───────────────
    STORY_OPENINGS = [
        "यह कहानी है {place} की, जहाँ {character} रहता था।",
        "बहुत समय पहले, {place} में एक {character} हुआ करता था।",
        "The story begins in {place}, where {character} lived a simple life.",
        "In the heart of {place}, there was a {character} unlike any other.",
        "किसी ने सोचा न था कि {place} में ऐसा कुछ होगा। {character} खुद भी हैरान था।",
    ]
    STORY_MIDDLE = [
        "एक दिन अचानक ऐसा हुआ कि {event}। यह देखकर सब दंग रह गए।",
        "But then, something unexpected happened: {event}. Everything changed.",
        "जिंदगी आसान थी, मगर {event} ने सब कुछ बदल दिया।",
        "And just when things seemed normal, {event} occurred.",
    ]
    STORY_ENDINGS = [
        "इस तरह {character} ने सीखा कि {lesson}। और फिर कभी पीछे मुड़कर नहीं देखा।",
        "And so, {character} understood that {lesson}. The end.",
        "आखिरकार, {character} को समझ आ ही गया कि {lesson} — यही असली जीत थी।",
        "In the end, {character} realized that {lesson}. A new chapter began.",
    ]

    def generate(self, query: str, atoms: list, style: str = 'auto') -> str:
        if not atoms:
            return f"मुझे इस बारे में और जानकारी चाहिए: {query}"

        response = random.choice(self.OPENERS)
        facts   = [a for a in atoms if a.atom_type == AtomType.FACT][:4]
        causal  = [a for a in atoms if a.atom_type == AtomType.CAUSAL][:2]
        rules   = [a for a in atoms if a.atom_type == AtomType.RULE][:2]

        for i, atom in enumerate(facts):
            template = random.choice(self.FACT_TEMPLATES)
            c = atom.content
            text = template.format(
                subject=c.get('subject', c.get('text', 'यह')),
                predicate=c.get('predicate', 'है'),
                object=c.get('object', c.get('text', 'महत्वपूर्ण'))
            )
            response += text + " "

        for atom in causal:
            template = random.choice(self.CAUSAL_TEMPLATES)
            response += template.format(**{k: v for k, v in atom.content.items() if k in ['cause','effect']}) + " "

        for atom in rules:
            template = random.choice(self.RULE_TEMPLATES)
            response += template.format(**{k: v for k, v in atom.content.items() if k in ['condition','conclusion']}) + " "

        return response.strip() + "."

    def generate_novel(self, prompt: str, length: int = 500) -> str:
        """Generate a creative story/novel based on the prompt.
        
        Args:
            prompt: Story topic or starting idea (e.g., "एक साधु की तपस्या")
            length: Approximate number of words to generate
        
        Returns:
            A complete creative story in natural human-like language
        """
        import random

        # Extract key elements from prompt
        words = prompt.split()
        character = words[0] if words else "नायक"
        place = words[-1] if len(words) > 1 else "एक गाँव"
        event = " ".join(words[2:5]) if len(words) > 4 else "एक रहस्यमय घटना"
        lesson = "सच्चाई और ईमानदारी ही सबसे बड़ी ताकत है"

        # Build story sections
        story_parts = []

        # Opening
        opening = random.choice(self.STORY_OPENINGS).format(
            place=place, character=character
        )
        story_parts.append(opening)

        # Middle sections
        target_words = length
        current_words = len(opening.split())

        middle_events = [
            f"{character} को एक पुरानी किताब मिली",
            f"आसमान में अजीब रोशनी दिखाई दी",
            f"गाँव में एक अनजान मेहमान आया",
            f"{character} ने एक गुप्त गुफा की खोज की",
            f"अचानक मौसम बदलने लगा",
        ]

        while current_words < target_words:
            event_choice = random.choice(middle_events)
            middle = random.choice(self.STORY_MIDDLE).format(event=event_choice)
            story_parts.append(middle)
            current_words += len(middle.split())

            # Add some detail
            detail = random.choice([
                f"हवा में एक अजीब सी खुशबू थी।",
                f"पक्षी चुप हो गए थे।",
                f"दूर कहीं घंटियाँ बज रही थीं।",
                f"{character} का दिल तेज़ी से धड़क रहा था।",
                f"यह सब देखकर {character} हैरान था, पर डरा नहीं।",
            ])
            story_parts.append(detail)
            current_words += len(detail.split())

            if current_words >= target_words * 0.7:
                break

        # Ending
        ending = random.choice(self.STORY_ENDINGS).format(
            character=character, lesson=lesson
        )
        story_parts.append(ending)

        return "

".join(story_parts)
