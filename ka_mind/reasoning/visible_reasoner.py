"""
Visible Reasoner - सिस्टम की सोच और लॉजिक को पारदर्शी (Transparent) बनाने वाला इंजन।
"""
import time
from typing import Tuple

class VisibleReasoner:
    def __init__(self, memory_graph):
        self.memory = memory_graph
        
    def think_and_answer(self, query: str, start_atom_id: str) -> Tuple[str, str]:
        """
        यह फंक्शन दो चीजें लौटाएगा:
        1. thought_process: सिस्टम ने कैसे सोचा (लॉजिक चेन)
        2. final_answer: यूजर के लिए सजी हुई भाषा में फाइनल जवाब
        """
        thoughts = []
        thoughts.append(f"🤔 [Thinking Process Started...]")
        thoughts.append(f"🔍 Analyzing Query: '{query}'")
        thoughts.append(f"🧠 Accessing Graph Memory (Entry Node: {start_atom_id})...")
        
        # गहराई (depth=2) तक जाकर जुड़े हुए सारे Knowledge Atoms निकालना
        context_nodes = self.memory.retrieve_context(start_atom_id, depth=2)
        
        if not context_nodes:
            thoughts.append("❌ No relevant Knowledge Atoms found in Graph.")
            return "\n".join(thoughts), "क्षमा करें, मेरे पास इस विषय पर पर्याप्त ज्ञान नहीं है।"
            
        thoughts.append(f"🔗 Retrieved {len(context_nodes)} connected Atoms from Neural Graph.")
        
        facts = []
        rules = []
        
        # निकाले गए Atoms का विश्लेषण करना
        for node_id, data in context_nodes:
            atom_type = data.get("type", "unknown")
            content = data.get("content", {})
            thoughts.append(f"   ↳ [Extracted {atom_type.upper()}]: {content}")
            
            if atom_type == "fact":
                facts.append(f"{content.get('subject')} {content.get('predicate')} {content.get('object')}")
            elif atom_type == "rule":
                rules.append(f"अगर {content.get('condition')}, तो {content.get('conclusion')}")

        thoughts.append("⚙️ Applying Logic: Combining Rules and Facts...")
        
        # फाइनल जवाब बनाना (Composer का शुरुआती रूप)
        thought_process = "\n".join(thoughts)
        
        final_answer = "मुझे अपने ज्ञान-ग्राफ से निम्नलिखित जानकारी मिली है:\n"
        if facts:
            final_answer += "• तथ्य: " + ", ".join(facts) + "।\n"
        if rules:
            final_answer += "• नियम: " + " और ".join(rules) + "।\n"
            
        return thought_process, final_answer
