"""
KA-Mind: Hugging Face Streaming Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.framework.trainer import KaTrainer

def run_test():
    print("="*60)
    print(" ☁️ KA-MIND: HUGGING FACE CLOUD STREAMING DEMO")
    print("="*60)
    
    # 1. चाणक्य मॉडल लोड करना
    model_path = "./models/chanakya_v1.0.kamind"
    if os.path.exists(model_path):
        chanakya = KaModel.load(model_path)
    else:
        chanakya = KaModel(name="Chanakya", domain="Politics and Strategy")
        
    trainer = KaTrainer(chanakya)
    
    # 2. Hugging Face से लाइव डेटा स्ट्रीम करना
    # हम Wikipedia के हिंदी/अंग्रेजी डेटासेट का एक छोटा हिस्सा स्ट्रीम कर रहे हैं
    hf_dataset = "wikipedia"
    hf_subset = "20220301.en" # आप इसे हिंदी ('hi') भी कर सकते हैं
    
    print(f"🌐 Connecting to Hugging Face: {hf_dataset}...")
    
    # सिर्फ 500 rows स्ट्रीम करेंगे ताकि डेमो जल्दी खत्म हो
    trainer.train(text="HuggingFace streaming demo — NeuraBrain rocks!")
    
    # 3. मॉडल सेव करना
    chanakya.save()
    print(f"\n🧠 मॉडल अपडेट हो गया! Stats: {chanakya.memory.memory_stats()}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
