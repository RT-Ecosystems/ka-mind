"""
KA-Mind: Model Factory Demo (चाणक्य मॉडल की ट्रेनिंग)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.framework.trainer import KaTrainer

def run_test():
    print("="*60)
    print(" 🏛️ KA-MIND FRAMEWORK: TRAINING 'CHANAKYA' MODEL")
    print("="*60)
    
    chanakya_model = KaModel(name="Chanakya", domain="Politics and Strategy")
    print(f"✨ नया मॉडल तैयार: {chanakya_model.name} (Domain: {chanakya_model.domain})")
    
    trainer = KaTrainer(chanakya_model)
    
    training_data = (
        "एक राजा को हमेशा अपनी प्रजा के हित में सोचना चाहिए. "
        "शत्रु की कमजोरी जानने के लिए गुप्तचरों का उपयोग सबसे उत्तम है. "
        "ज्ञान ही मनुष्य की सबसे बड़ी शक्ति है, इसे कभी नहीं छोड़ना चाहिए."
    )
    
    trainer.train_from_text(training_data)
    
    saved_path = chanakya_model.save()
    print(f"💾 मॉडल यहाँ सेव हो गया: {saved_path}")
    
    print("\n" + "-"*40)
    print("🧠 चाणक्य का टेस्ट (Inference):")
    print(f"Stats: {chanakya_model.memory.memory_stats()}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
