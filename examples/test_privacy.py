"""
KA-Mind: Real-time Learning & Privacy Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.core.graph_memory import GraphMemory
from ka_mind.agents.web_agent import WebAgent
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

def run_test():
    print("="*60)
    print(" 🔒 KA-MIND: CONTINUOUS LEARNING & PRIVACY DEMO")
    print("="*60)
    
    memory = GraphMemory()
    web_agent = WebAgent(memory)
    
    # ── Scene 1: राहुल (User 1) की प्राइवेट बात ──
    print("👤 [राहुल]: 'मेरी गर्लफ्रेंड का नाम अंजलि है।'")
    rahul_secret = KnowledgeAtom(AtomType.FACT, {"text": "राहुल की गर्लफ्रेंड अंजलि है।"}, scope="private", user_id="user_rahul")
    memory.add_atom(rahul_secret)
    print("🧠 सिस्टम ने इसे 'Private' सेव कर लिया।")
    
    # ── Scene 2: राहुल (User 1) इंटरनेट से सवाल पूछता है ──
    print("\n👤 [राहुल]: 'भारत की GDP क्या है?'")
    print("🌐 " + web_agent.search_and_learn("भारत की GDP"))
    
    print("\n" + "-"*40)
    
    # ── Scene 3: अमित (User 2) आता है (Privacy Test) ──
    print("👤 [अमित]: 'भारत की GDP क्या है?'")
    gdp_result = memory.search("gdp", current_user_id="user_amit")
    print(f"🤖 [KA-Mind]: {gdp_result[0].content['text']} (वेब सर्च के बिना पुराने ज्ञान से जवाब दिया!)")
    
    print("\n👤 [अमित]: 'राहुल की गर्लफ्रेंड कौन है?'")
    secret_result = memory.search("गर्लफ्रेंड", current_user_id="user_amit")
    if not secret_result:
        print("🤖 [KA-Mind]: माफ़ करें, मुझे इसकी कोई जानकारी नहीं है। (🔒 Privacy Protected!)")
    else:
        print("❌ Error: प्राइवेसी टूट गई!")
        
    print(f"\n📊 Memory Status: {memory.memory_stats()}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
