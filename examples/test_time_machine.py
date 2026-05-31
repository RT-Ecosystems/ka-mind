"""
KA-Mind: Temporal Reasoning Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.core.temporal_atom import TemporalAtom
from ka_mind.core.temporal_reasoner import TemporalReasoner

def run_test():
    print("="*60)
    print(" ⏳ KA-MIND: TEMPORAL REASONING (TIME MACHINE) DEMO")
    print("="*60)
    
    time_engine = TemporalReasoner()
    
    # 1. इतिहास और वर्तमान का डेटा डालना (LLMs यहाँ कंफ्यूज होते हैं)
    print("📥 [Ingestion]: समय के अलग-अलग पड़ाव का डेटा फीड किया जा रहा है...")
    time_engine.add_event(TemporalAtom("भारत के प्रधानमंत्री मनमोहन सिंह हैं।", year=2010, is_current=False))
    time_engine.add_event(TemporalAtom("भारत के प्रधानमंत्री नरेंद्र मोदी हैं।", year=2014, is_current=True))
    time_engine.add_event(TemporalAtom("भारत के प्रधानमंत्री नरेंद्र मोदी फिर से चुने गए।", year=2024, is_current=True))
    
    print("\n" + "-"*40)
    
    # 2. समय का टेस्ट!
    print("👤 [User]: 2012 में भारत का प्रधानमंत्री कौन था?")
    print(time_engine.ask_question("प्रधानमंत्री", target_year=2012))
    
    print("\n👤 [User]: वर्तमान में (आज) भारत का प्रधानमंत्री कौन है?")
    print(time_engine.ask_question("प्रधानमंत्री")) # बिना साल के पूछा
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
