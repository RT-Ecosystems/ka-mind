"""
KA-Mind: Checkpoint, Resume & Deduplication Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.framework.trainer import KaTrainer

def run_test():
    print("="*60)
    print(" 🛡️ KA-MIND: CHECKPOINT & DEDUPLICATION DEMO")
    print("="*60)
    
    chanakya = KaModel(name="Chanakya", domain="Politics and Strategy")
    trainer = KaTrainer(chanakya)
    
    print("🎬 [Round 1]: पहली बार ट्रेनिंग शुरू हो रही है...")
    # हम सिर्फ 200 लाइनों का डेमो कर रहे हैं
    trainer.train_from_huggingface("wikipedia", text_column="text", max_rows=200)
    
    print("\n💥 [Simulation]: मान लीजिए सर्वर यहाँ क्रैश हो गया और बंद हो गया!")
    print("-" * 60)
    
    print("\n🔄 [Round 2]: सर्वर वापस चालू हुआ। अब हम कोड फिर से रन कर रहे हैं...")
    # नया ट्रेनर और मॉडल ऑब्जेक्ट (मानो सब रीस्टार्ट हो गया हो)
    chanakya_rebooted = KaModel.load("./checkpoints/chanakya/chanakya_v1.0.kamind")
    trainer_rebooted = KaTrainer(chanakya_rebooted)
    
    # यह फिर से वहीं से शुरू होगा जहाँ रुका था!
    trainer_rebooted.train_from_huggingface("wikipedia", text_column="text", max_rows=200)
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
