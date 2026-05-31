"""
KA-Mind: CPU Parallel Processing Demo
"""
import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.model import KaModel
from ka_mind.framework.trainer import KaTrainer

def run_test():
    print("="*60)
    print(" ⚡ KA-MIND: MULTIPROCESSING TRAINING DEMO")
    print("="*60)
    
    chanakya = KaModel(name="Chanakya_Turbo", domain="Strategy")
    trainer = KaTrainer(chanakya)
    
    # एक 20,000 लाइनों की डमी फाइल बनाना
    test_file = "massive_test_data.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        for i in range(20000):
            f.write(f"यह एक महत्वपूर्ण तथ्य है संख्या {i} जो पैरेलल प्रोसेस होगा। चाणक्य ने कहा था समय ही धन है।\n")
            
    print(f"📝 {os.path.getsize(test_file) / 1024 / 1024:.2f} MB की डमी फाइल तैयार।")
    
    # टाइमर चालू
    start_time = time.time()
    
    # पैरेलल ट्रेनिंग रन करना
    trainer.train_parallel(test_file, chunk_size=10000)
    
    end_time = time.time()
    print(f"⏱️ कुल समय: {end_time - start_time:.2f} सेकंड्स!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
