"""
KA-Mind: Sleep Cycle Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ka_mind.core.graph_memory import GraphMemory
from ka_mind.memory.optimizer import MemoryOptimizer

def run_test():
    memory = GraphMemory()
    optimizer = MemoryOptimizer(memory)
    
    print("="*60)
    print("🌙 KA-MIND: SLEEP CYCLE & MEMORY OPTIMIZATION DEMO")
    print("="*60)
    
    # User की पूरी चैट हिस्ट्री
    chat_history = [
        "नमस्ते", 
        "क्या हाल है?", 
        "मेरा एक नया प्रोजेक्ट है AI पर।", 
        "ओके", 
        "मैं कल इस पर काम करूंगा।"
    ]
    
    output = optimizer.run_sleep_cycle(chat_history)
    print("\n" + output)
    
    print(f"\n📊 After Sleep Cycle: {memory.memory_stats()}")
    print("नोट: 'नमस्ते' और 'ओके' डिलीट हो गए, लेकिन प्रोजेक्ट की जानकारी परमानेंट सेव हो गई!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_test()
