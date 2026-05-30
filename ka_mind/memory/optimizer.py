"""
Memory Optimizer - KA-Mind का 'Sleep Cycle'.
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class MemoryOptimizer:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def run_sleep_cycle(self, raw_chat_history: list) -> str:
        """चैट से काम के फैक्ट्स निकालना और फालतू चीजें भूलना"""
        thoughts = ["🌙 [Sleep Cycle Activated]: Analyzing Chat History..."]
        
        useless_words = ["hi", "hello", "ok", "नमस्ते", "हां", "ना", "ठीक है", "goodnight"]
        saved_facts = 0
        
        for msg in raw_chat_history:
            msg_lower = msg.lower().strip()
            # फालतू डेटा तुरंत डिलीट (RAM बच गई)
            if msg_lower in useless_words or len(msg_lower) < 10:
                continue 
            
            # काम की बात को Permanent Atom बनाना
            if any(word in msg_lower for word in ["मेरा", "मैं", "मुझे", "प्रोजेक्ट"]):
                atom = KnowledgeAtom(AtomType.FACT, {"user_data": msg}, source="user_chat", category="user_profile")
                if self.memory.add_atom(atom):
                    saved_facts += 1
                    
        thoughts.append(f"🧹 कचरा साफ किया गया। {saved_facts} महत्वपूर्ण तथ्य Permanent Memory में सेव किए गए!")
        thoughts.append("💤 Sleep Cycle Complete. 100% Memory Maintained.")
        
        return "\n".join(thoughts)
