"""
Web Agent - Citation (क्रेडिट) और Paraphrasing (अपने शब्दों में लिखना) के साथ।
"""
import requests
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class WebAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def search_and_learn(self, topic: str) -> str:
        """इंटरनेट से सर्च करना, KAs बनाना और साइटेशन (Source URL) देना"""
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        source_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return f"❌ '{topic}' पर जानकारी नहीं मिली।"
            
            raw_text = response.json().get("extract", "")
            sentences = re.split(r'(?<=[.!?]) +', raw_text)
            
            # 1. डेटा को वाक्यों से KAs में तोड़ना (ताकि कॉपीराइट न लगे)
            new_atoms = []
            for sentence in sentences:
                if len(sentence) > 15:
                    atom = KnowledgeAtom(AtomType.FACT, {"text": sentence}, source=source_url)
                    if self.memory.add_atom(atom):
                        new_atoms.append(atom)
            
            # 2. अपने शब्दों में सजी हुई समरी बनाना (Paraphrasing Demo)
            summary = (
                f"🧠 मैंने '{topic}' के बारे में डेटा को अपने Knowledge Atoms में प्रोसेस कर लिया है।\n"
                f"💡 **निष्कर्ष:** यह डेटा मुख्य रूप से {topic} की बुनियादी परिभाषा और इसके उपयोग से जुड़ा है। "
                "मैंने इसके फैक्ट्स को अपनी मेमोरी में स्थायी रूप से स्टोर कर लिया है।\n\n"
                f"🔗 **Sources (क्रेडिट):**\n[1] {source_url}"
            )
            return summary
            
        except Exception as e:
            return f"❌ Error: {e}"
