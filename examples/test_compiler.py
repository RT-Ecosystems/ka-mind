"""
KA-Mind: Brain Compiler Demo
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.framework.compiler import KaCompiler

def run_test():
    print("="*60)
    print(" 🏭 KA-MIND: BRAIN COMPILER & OPTIMIZER DEMO")
    print("="*60)
    
    # चेक करते हैं कि क्या Phase 14 का चेकपॉइंट मौजूद है
    checkpoint_file = "./checkpoints/chanakya/chanakya_v1.0.kamind"
    
    if not os.path.exists(checkpoint_file):
        print(f"❌ Error: {checkpoint_file} नहीं मिला। पहले Phase 14 रन करें।")
        return
        
    # 1. कंपाइलर को चेकपॉइंट देना
    compiler = KaCompiler(checkpoint_path=checkpoint_file)
    
    # 2. कंपाइल करना और फाइनल रिलीज़ बनाना
    final_file = compiler.optimize_and_compile(version="1.0_PRODUCTION")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    run_test()
