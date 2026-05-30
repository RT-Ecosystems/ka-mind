"""
Web Agent - DuckDuckGo सर्च इंजन के साथ (Robust & Real-time)।
"""
import urllib.request
import urllib.parse
import json
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class WebAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def search_and_learn(self, topic: str) -> str:
        """DuckDuckGo से सर्च करना, KAs बनाना और साइटेशन देना"""
        thoughts = []
        thoughts.append(f"🌐 [Web Agent Activated]: DuckDuckGo पर '{topic}' सर्च किया जा रहा है...")
        
        try:
            # DuckDuckGo API URL Setup
            enc = urllib.parse.quote(topic)
            url = f"https://api.duckduckgo.com/?q={enc}&format=json&no_html=1"
            req = urllib.request.Request(url, headers={"User-Agent": "KA-Mind/1.0"})
            
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                
            raw_text = data.get("AbstractText", "")
            source_url = data.get("AbstractURL", "")
            
            # अगर Abstract खाली है, तो Related Topics से डेटा उठाओ
            if not raw_text:
                for t in data.get("RelatedTopics", []):
                    if isinstance(t, dict) and "Text" in t:
                        raw_text += t["Text"] + ". "
                        if not source_url:
                            source_url = t.get("FirstURL", "DuckDuckGo")
                        break
                        
            if not raw_text.strip():
                return f"❌ माफ़ करें, '{topic}' पर कोई सीधा जवाब नहीं मिला।"
                
            thoughts.append(f"📖 [Data Extracted]: डेटा मिल गया। Processing into Atoms...")
            
            # डेटा को वाक्यों से KAs में तोड़ना
            sentences = re.split(r'(?<=[.!?]) +', raw_text)
            new_atoms_count = 0
            
            for sentence in sentences:
                if len(sentence) > 15:
                    atom = KnowledgeAtom(AtomType.FACT, {"text": sentence}, source=source_url)
                    if self.memory.add_atom(atom):
                        new_atoms_count += 1
                        
            thoughts.append(f"🧠 [Learning Complete]: {new_atoms_count} नए Knowledge Atoms ग्राफ में जोड़ दिए गए!")
            
            # फाइनल आउटपुट
            summary = (
                f"{chr(10).join(thoughts)}\n\n"
                f"💡 **निष्कर्ष (KA-Mind Summary):**\n{raw_text[:300]}...\n\n"
                f"🔗 **Source:** [1] {source_url}"
            )
            return summary
            
        except Exception as e:
            return f"❌ Search Error: {e}"
