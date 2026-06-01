"""
KA-Mind: Advanced Cognition Demo (Concept, Rules & Ranking)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.core.abstractor import Abstractor
from ka_mind.core.world_model import WorldModel
from ka_mind.memory.optimizer import MemoryRanker
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

def run_test():
    print("="*60)
    print(" 🌌 KA-MIND: ADVANCED COGNITIVE CORE DEMO")
    print("="*60)
    
    model = KaModel(name="Chanakya_Ultimate")
    abstractor = Abstractor(model.memory)
    world_model = WorldModel(model.memory)
    ranker = MemoryRanker(model.memory)
    
    # 1. डमी डेटा डालना
    print("📥 [Ingestion]: कच्चा डेटा डाला जा रहा है...")
    facts = [
        "कुत्ता भोंकता है।", "कुत्ता दौड़ता है।", "कुत्ता वफादार होता है।", "कुत्ता दूध पीता है।",
        "सूरज हमेशा पूरब से निकलता है।", "आग हमेशा गर्म होती है।"
    ]
    for f in facts:
        model.memory.add_atom(KnowledgeAtom(AtomType.FACT, {"text": f}))
        
    print("\n" + "-"*40)
    
    # 2. Compression (Concept Creation)
    print("1. Knowledge Compression Test:")
    for concept in abstractor.create_concepts(): print(concept)
    
    # 3. Rule Discovery & World Model
    print("\n2. Rule Discovery & Simulation Test:")
    for rule in world_model.discover_rules(): print(rule)
    print(world_model.simulate_what_if("अगर सूरज गायब हो जाए?"))
    
    # 4. Memory Ranking
    print("\n3. Memory Ranking (Evidence System) Test:")
    print(ranker.rank_memories())
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
