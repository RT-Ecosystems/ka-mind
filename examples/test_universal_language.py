"""
KA-Mind: Universal Vector Language Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.core.vector_atom import VectorAtom
from ka_mind.core.vector_graph import VectorGraph

def run_test():
    print("="*60)
    print(" 🌍 KA-MIND: UNIVERSAL LANGUAGE (VECTOR) DEMO")
    print("="*60)
    
    memory = VectorGraph()
    
    # 1. मॉडल को हिंदी में ज्ञान देना
    print("📥 [Ingestion - Hindi]: सिस्टम को हिंदी में सिखाया जा रहा है...")
    hindi_fact = VectorAtom("पानी का रंग नीला होता है।")
    memory.add_atom(hindi_fact)
    print(f"🧬 [Universal Vector Generated]: {hindi_fact.get_universal_meaning()}...")
    
    print("\n" + "-"*40)
    
    # 2. अन्य भाषाओं में सवाल पूछना (The Magic Test!)
    print("🗣️ [User - English]: 'What is the color of water?'")
    match, score = memory.search_by_meaning("What is the color of water?")
    print(f"🤖 [Match Found! Score: {score:.2f}]: '{match.text}'")
    
    print("\n🗣️ [User - French]: 'Quelle est la couleur de l'eau?'")
    match, score = memory.search_by_meaning("Quelle est la couleur de l'eau?")
    print(f"🤖 [Match Found! Score: {score:.2f}]: '{match.text}'")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
