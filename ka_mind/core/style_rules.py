"""
StyleRules — Creative writing styles for FluidComposer.
Teaches: Poetry, Satire, Description, Dialogue, Formal, Casual.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random


@dataclass
class StyleProfile:
    """A writing style profile."""
    name: str
    description: str
    sentence_length: str = "medium"  # short, medium, long
    tone: str = "neutral"            # formal, casual, poetic, satirical
    openers: List[str] = field(default_factory=list)
    structures: List[str] = field(default_factory=list)
    endings: List[str] = field(default_factory=list)


class StyleRules:
    """Registry of writing styles for creative generation."""

    PROFILES: Dict[str, StyleProfile] = {
        "poetry": StyleProfile(
            name="poetry",
            description="कविता / Poetry style",
            sentence_length="short",
            tone="poetic",
            openers=[
                "चाँद की रोशनी में,", "In the stillness of night,",
                "हवा की सरसराहट में,", "Like a gentle breeze,",
                "दिल की गहराइयों से,", "From the depths of silence,",
            ],
            structures=[
                "{line1},
{line2},
{line3} —
{line4}।",
                "{line1}...
{line2} की तरह,
{line3}।",
                "O {subject}, you are {object},
A {adjective} presence in the {place}.",
            ],
            endings=[
                "बस इतना ही...", "And so it goes...",
                "यही तो है ज़िंदगी।", "Such is the way of things.",
            ]
        ),
        "satire": StyleProfile(
            name="satire",
            description="व्यंग्य / Satire style",
            sentence_length="medium",
            tone="satirical",
            openers=[
                "देखिए न,", "Well, well, well...",
                "यह तो और भी मज़ेदार है —", "Isn't it amusing that",
                "आश्चर्य की बात है कि", "How fascinating that",
            ],
            structures=[
                "{statement}. और हम कहते हैं कि {irony}।",
                "They say {statement}. {irony}, isn't it?",
                "क्या मज़ाक है: {statement}. हकीकत: {irony}।",
            ],
            endings=[
                "समझ गए ना?", "Need I say more?",
                "बाकी आप खुद समझदार हैं।", "The rest, as they say, is commentary.",
            ]
        ),
        "description": StyleProfile(
            name="description",
            description="वर्णन / Descriptive style",
            sentence_length="long",
            tone="formal",
            openers=[
                "देखने पर पता चलता है कि", "Upon observation,",
                "यह एक ऐसा स्थान है जहाँ", "It is a place where",
                "विस्तार से देखें तो", "In detail,",
            ],
            structures=[
                "{subject} एक {adjective} {object} है, जो {detail1} और {detail2} से भरपूर है।",
                "The {subject} stands as a {adjective} {object}, rich with {detail1} and {detail2}.",
            ],
            endings=[
                "यही इसकी खूबसूरती है।", "Such is its beauty.",
            ]
        ),
        "dialogue": StyleProfile(
            name="dialogue",
            description="संवाद / Dialogue style",
            sentence_length="short",
            tone="casual",
            openers=[
                '"अरे, सुनो तो —"', '"Hey, listen —"',
                '"क्या बात है!"', '"What's going on!"',
                '"अच्छा? तो ऐसी बात है..."', '"Oh? Is that so..."',
            ],
            structures=[
                '"{line1}", उसने कहा।
"{line2}", दूसरे ने जवाब दिया।',
                '"{line1}", they said.
"{line2}", came the reply.',
            ],
            endings=[
                '"चलो, फिर मिलते हैं!"', '"See you around!"',
            ]
        ),
        "formal": StyleProfile(
            name="formal",
            description="औपचारिक / Formal style",
            sentence_length="long",
            tone="formal",
            openers=[
                "यह ज्ञात है कि", "It is known that",
                "इस संदर्भ में,", "In this context,",
                "विशेषज्ञों के अनुसार,", "According to experts,",
            ],
            structures=[
                "{subject} एक महत्वपूर्ण {object} है, जिसका अध्ययन {field} में किया जाता है।",
                "{subject} is an important {object}, studied in the field of {field}.",
            ],
            endings=[
                "यह आगे के शोध का विषय है।", "This remains a subject for further study.",
            ]
        ),
        "casual": StyleProfile(
            name="casual",
            description="आम बोलचाल / Casual style",
            sentence_length="short",
            tone="casual",
            openers=[
                "यार,", "अरे भाई,", "सुनो ना,",
                "You know what,", "Hey,", "So,",
            ],
            structures=[
                "{statement}. मतलब, {casual_explanation}.",
                "{statement}. I mean, {casual_explanation}.",
            ],
            endings=[
                "तो ये बात है।", "So that's the thing.",
                "समझ गए ना?", "Got it?",
            ]
        ),
    }

    @classmethod
    def get(cls, style_name: str) -> Optional[StyleProfile]:
        return cls.PROFILES.get(style_name, cls.PROFILES.get("casual"))

    @classmethod
    def available_styles(cls) -> List[str]:
        return list(cls.PROFILES.keys())
