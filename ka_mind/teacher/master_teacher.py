"""
Master Teacher Script - KA-Mind का मुख्य आर्किटेक्ट।
"""
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class MasterTeacher:
    def __init__(self, memory_graph, web_agent=None, code_agent=None):
        self.memory = memory_graph
        self.web_agent = web_agent
        self.code_agent = code_agent
        
    def process_request(self, user_query: str) -> str:
        if self._is_copyright_risk(user_query):
            return self._handle_copyright_block()
            
        intent = self._analyze_intent(user_query)
        
        if intent == "build_code":
            if self.code_agent:
                return self.code_agent.solve_task(user_query)
            return "❌ Code Agent is offline."
            
        elif intent == "web_search":
            if self.web_agent:
                # यूजर के सवाल में से मुख्य टॉपिक निकालना (Simple Extraction)
                topic = user_query.replace("सर्च करो", "").replace("के बारे में बताओ", "").replace("internet", "").strip()
                return self.web_agent.search_and_learn(topic)
            return "❌ Web Agent is offline."
            
        else:
            return self._learn_and_reason(user_query)

    def _is_copyright_risk(self, text: str) -> bool:
        text = text.lower()
        risk_keywords = ["पूरा चैप्टर", "पूरी कहानी", "chapter", "novel", "उपन्यास", "lyrics", "किताब", "book", "हुबहू", "verbatim"]
        return any(word in text for word in risk_keywords)

    def _handle_copyright_block(self) -> str:
        return (
            "🛡️ [Copyright Shield]: मैं कॉपीराइट कानूनों का सम्मान करता हूँ। "
            "मैं पूरा टेक्स्ट (हूबहू) नहीं दे सकता, लेकिन मैं इसके मुख्य फैक्ट्स (Knowledge Atoms) बता सकता हूँ।"
        )

    def _analyze_intent(self, text: str) -> str:
        text = text.lower()
        if any(word in text for word in ["बनाओ", "कोड", "वेबसाइट", "कैलकुलेशन", "build", "code", "script"]):
            return "build_code"
        elif any(word in text for word in ["सर्च", "इंटरनेट", "news", "current", "के बारे में बताओ"]):
            return "web_search"
        return "general_reasoning"
        
    def _learn_and_reason(self, query: str) -> str:
        # यहाँ हमारा Visible Reasoner काम करेगा (Phase 2 वाला)
        return "🧠 [Thinking]: मेरे पास अभी इस सवाल का सटीक संदर्भ नहीं है। आप मुझसे इंटरनेट सर्च करने या कोड लिखने को कह सकते हैं!"
