"""
Master Teacher Script - KA-Mind का मुख्य आर्किटेक्ट।
यह तय करता है कि डेटा कैसे पढ़ना है, टूल्स का इस्तेमाल कब करना है, और ज्ञान को कैसे मर्ज करना है।
"""
import re
from typing import Dict, Any
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class MasterTeacher:
    def __init__(self, memory_graph):
        self.memory = memory_graph
        # भविष्य के एजेंट्स के लिए प्लेसहोल्डर
        self.web_agent = None 
        self.code_agent = None

    def process_request(self, user_query: str) -> str:
        """यूजर के सवाल का विश्लेषण करके सही एक्शन लेना"""
        intent = self._analyze_intent(user_query)
        
        if intent == "build_code":
            return self._handle_coding_task(user_query)
        elif intent == "web_search":
            return self._handle_web_search(user_query)
        else:
            return self._learn_and_reason(user_query)

    def _analyze_intent(self, text: str) -> str:
        """समझना कि यूजर कोडिंग चाहता है, रियल-टाइम सर्च चाहता है, या सिर्फ बातचीत"""
        text = text.lower()
        if any(word in text for word in ["बनाओ", "कोड", "वेबसाइट", "build", "code", "script"]):
            return "build_code"
        elif any(word in text for word in ["आज", "सर्च", "इंटरनेट", "news", "current", "क्या चल रहा है"]):
            return "web_search"
        return "general_reasoning"

    def _handle_coding_task(self, query: str) -> str:
        """कोडिंग टास्क को हैंडल करना और Code Agent को सिखाना"""
        # यहाँ Code Agent का इस्तेमाल होगा (Phase 4 में असली Sandbox बनेगा)
        response = f"🛠️ [Master Teacher]: मैंने पहचान लिया है कि आपको कोडिंग (जैसे वेबसाइट बनाना) की जरूरत है।\n"
        response += "↳ Code Agent को सक्रिय किया जा रहा है... (कोड जनरेट और टेस्ट किया जाएगा)\n"
        response += "↳ [Mock Output]: <html><body><h1>Hello KA-Mind</h1></body></html>"
        return response

    def _handle_web_search(self, query: str) -> str:
        """इंटरनेट से डेटा मंगाना, उसे साफ करना और ग्राफ में डालना"""
        # यहाँ Web Agent काम करेगा
        response = f"🌐 [Master Teacher]: मेरे ग्राफ में यह डेटा नहीं है। मैं इंटरनेट स्कैन कर रहा हूँ...\n"
        response += "↳ Web Agent ने डेटा निकाला। Teacher Script इसे फिल्टर कर रही है...\n"
        
        # डेमो के लिए: इंटरनेट से मिला एक नया फैक्ट हम मेमोरी में मर्ज कर रहे हैं
        new_fact = KnowledgeAtom(AtomType.FACT, {"subject": "नया डेटा", "predicate": "है", "object": "अपडेटेड"}, source="web")
        is_new = self.memory.add_atom(new_fact)
        
        if is_new:
            response += f"↳ 🧠 नया ज्ञान (Atom ID: {new_fact.atom_id}) मेमोरी ग्राफ में स्थायी रूप से सेव कर लिया गया!\n"
        else:
            response += "↳ ♻️ यह ज्ञान पहले से था, इसलिए डुप्लीकेट नहीं बनाया गया (Memory Saved!).\n"
            
        return response

    def stream_and_merge_data(self, raw_text: str):
        """
        विशाल डेटा को हैंडल करना: 
        जब हम इसे 100TB डेटा देंगे, तो यह कचरा हटाकर सिर्फ शुद्ध KAs बनाएगा।
        """
        sentences = re.split(r'(?<=[.!?]) +', raw_text)
        atoms_added = 0
        
        for sentence in sentences:
            if len(sentence) > 10:
                # बेसिक फैक्ट एक्सट्रैक्शन (एडवांस NLP बाद में जुड़ेगा)
                atom = KnowledgeAtom(AtomType.FACT, {"text": sentence}, source="stream")
                if self.memory.add_atom(atom):
                    atoms_added += 1
                    
        return f"स्ट्रीमिंग पूरी हुई। {len(sentences)} वाक्यों में से {atoms_added} नए Atoms ग्राफ में जोड़े गए।"
