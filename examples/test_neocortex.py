"""
KA-Mind: Neocortex Demo (Reasoning & Contradictions)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.framework.trainer import KaTrainer
from ka_mind.core.neocortex import Neocortex

def run_test():
    print("="*60)
    print(" 🧠 KA-MIND: NEOCORTEX (THE PAPA AI) DEMO")
    print("="*60)
    
    # 1. मॉडल और ट्रेनर तैयार करना
    model = KaModel(name="Chanakya_Pro")
    trainer = KaTrainer(model)
    neocortex = Neocortex(model.memory)
    
    # 2. उसे कुछ कच्चा डेटा देना (जिसमें राज़ और टकराव छिपे हैं)
    training_data = (
        "कौवा एक पक्षी है. "
        "पक्षियों के पंख होते हैं. "
        "प्लूटो एक ग्रह है. "
        "प्लूटो एक ग्रह नहीं है. "
    )
    
    print("📥 [Ingestion]: मॉडल को कच्चा डेटा खिलाया जा रहा है...")
    trainer.train_from_text(training_data)
    
    # 3. अब Neocortex का जादू देखना (Deep Sleep Mode)
    print("\n" + "-"*60)
    print("✨ अब सिस्टम अपना दिमाग (Neocortex) इस्तेमाल करेगा:")
    neocortex.run_deep_sleep_cycle()
    print("-" * 60 + "\n")

if __name__ == "__main__":
    run_test()
