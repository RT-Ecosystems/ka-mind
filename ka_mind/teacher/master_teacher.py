"""
Master Teacher Script - Updated with Vision Agent
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class MasterTeacher:
    def __init__(self, memory_graph, web_agent=None, code_agent=None, vision_agent=None):
        self.memory = memory_graph
        self.web_agent = web_agent
        self.code_agent = code_agent
        self.vision_agent = vision_agent
        
    def process_request(self, user_query: str) -> str:
        intent = self._analyze_intent(user_query)
        
        if intent == "draw_image":
            if self.vision_agent:
                prompt = user_query.replace("बनाओ", "").replace("इमेज", "").replace("एक", "").strip()
                return self.vision_agent.generate_image(prompt)
            return "❌ Vision Agent is offline."
            
        elif intent == "build_code":
            if self.code_agent:
                return self.code_agent.solve_task(user_query)
            return "❌ Code Agent is offline."
            
        elif intent == "web_search":
            if self.web_agent:
                topic = user_query.replace("सर्च करो", "").replace("के बारे में बताओ", "").strip()
                return self.web_agent.search_and_learn(topic)
            return "❌ Web Agent is offline."
            
        return "🧠 [Thinking]: मेरे पास अभी इस सवाल का सटीक संदर्भ नहीं है।"

    def _analyze_intent(self, text: str) -> str:
        text = text.lower()
        if any(word in text for word in ["इमेज", "फोटो", "पिक्चर", "draw", "image", "picture"]):
            return "draw_image"
        elif any(word in text for word in ["कोड", "कैलकुलेशन", "build", "code"]):
            return "build_code"
        elif any(word in text for word in ["सर्च", "इंटरनेट", "के बारे में बताओ"]):
            return "web_search"
        return "general_reasoning"
