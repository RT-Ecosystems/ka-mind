"""
KA-Mind: Live Reasoning Test
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
from ka_mind.core.graph_memory import GraphMemory
from ka_mind.reasoning.visible_reasoner import VisibleReasoner

def run_test():
    print("\n" + "="*50)
    print("🧠 KA-MIND: LIVE REASONING TEST")
    print("="*50)
    
    # 1. मेमोरी ग्राफ बनाना
    memory = GraphMemory()
    
    # 2. कुछ Knowledge Atoms बनाना (हम इसे मैन्युअली बना रहे हैं, बाद में Web Agent खुद बनाएगा)
    atom1 = KnowledgeAtom(AtomType.FACT, {"subject": "बारिश", "predicate": "होने पर", "object": "पानी गिरता है"})
    atom2 = KnowledgeAtom(AtomType.RULE, {"condition": "पानी गिरता है", "conclusion": "जमीन गीली हो जाती है"})
    atom3 = KnowledgeAtom(AtomType.CAUSAL, {"cause": "जमीन गीली होना", "effect": "फिसलन बढ़ जाती है"})
    
    # ग्राफ में जोड़ना
    memory.add_atom(atom1)
    memory.add_atom(atom2)
    memory.add_atom(atom3)
    
    # उनके बीच संबंध (Edges) बनाना
    memory.add_relation(atom1.atom_id, atom2.atom_id, "triggers")
    memory.add_relation(atom2.atom_id, atom3.atom_id, "causes")
    
    # 3. Reasoning Engine को चालू करना
    reasoner = VisibleReasoner(memory)
    
    query = "क्या बारिश होने पर हमें संभलकर चलना चाहिए?"
    print(f"\n👤 USER QUERY: {query}\n")
    
    # प्रोसेस रन करना
    thoughts, answer = reasoner.think_and_answer(query, atom1.atom_id)
    
    print(thoughts)
    print("\n" + "-"*50)
    print(f"🤖 FINAL ANSWER:\n{answer}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_test()
