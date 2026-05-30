"""
Master Teacher Script - KA-Mind का मुख्य आर्किटेक्ट (With Copyright Shield)।
"""
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class MasterTeacher:
    def __init__(self, memory_graph):
        self.memory = memory_graph
        
    def process_request(self, user_query: str) -> str:
        """यूजर के सवाल का विश्लेषण करके सही एक्शन लेना"""
        
        # 1. सबसे पहले Copyright Risk चेक करना
        if self._is_copyright_risk(user_query):
            return self._handle_copyright_block(user_query)
            
        intent = self._analyze_intent(user_query)
        
        if intent == "build_code":
            return self._handle_coding_task(user_query)
        elif intent == "web_search":
            return self._handle_web_search(user_query)
        else:
            return self._learn_and_reason(user_query)

    def _is_copyright_risk(self, text: str) -> bool:
        """चेक करना कि क्या यूजर पूरा चैप्टर, नॉवेल, या लिरिक्स मांग रहा है"""
        text = text.lower()
        risk_keywords = ["पूरा चैप्टर", "पूरी कहानी", "chapter", "novel", "उपन्यास", "lyrics", "किताब", "book", "हुबहू", "verbatim"]
        return any(word in text for word in risk_keywords)

    def _handle_copyright_block(self, query: str) -> str:
        """कॉपीराइट वाले सवालों को ग्रेसफुली हैंडल करना"""
        return (
            "🛡️ [Copyright Shield Activated]:\n"
            "मैं कॉपीराइट कानूनों और 'Fair Use' पॉलिसी का सम्मान करता हूँ। "
            "इसलिए, मैं किसी नॉवेल, किताब, या लेख का पूरा टेक्स्ट (हूबहू) नहीं दे सकता।\n"
            "💡 हालांकि, मैं आपके लिए इसे पढ़कर इसकी एक बेहतरीन **समरी (Summary)** बना सकता हूँ या इसके मुख्य **फैक्ट्स (Knowledge Atoms)** बता सकता हूँ। क्या आप वह चाहेंगे?"
        )

    def _analyze_intent(self, text: str) -> str:
        text = text.lower()
        if any(word in text for word in ["बनाओ", "कोड", "वेबसाइट", "build", "code", "script"]):
            return "build_code"
        elif any(word in text for word in ["आज", "सर्च", "इंटरनेट", "news", "current"]):
            return "web_search"
        return "general_reasoning"

    def _handle_coding_task(self, query: str) -> str:
        return "🛠️ [Code Agent Task Delegated]"

    def _handle_web_search(self, query: str) -> str:
        return "🌐 [Web Agent Task Delegated]"
        
    def _learn_and_reason(self, query: str) -> str:
        return "🧠 [Thinking and Reasoning...]"
