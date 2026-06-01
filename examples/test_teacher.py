"""
KA-Mind: Master Teacher Test
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ka_mind.core.graph_memory import GraphMemory
from ka_mind.teacher.master_teacher import MasterTeacher

def run_test():
    memory = GraphMemory()
    teacher = MasterTeacher(memory)
    
    print("="*50)
    print("🎓 KA-MIND: MASTER TEACHER SCRIPT DEMO")
    print("="*50)
    
    # 1. कोडिंग टेस्ट
    print("\n👤 USER: मेरे लिए एक ई-कॉमर्स वेबसाइट का कोड बनाओ।")
    print(teacher.process_request("मेरे लिए एक ई-कॉमर्स वेबसाइट का कोड बनाओ।"))
    
    # 2. वेब सर्च टेस्ट
    print("\n👤 USER: इंटरनेट पर सर्च करो कि आज क्या न्यूज है।")
    print(teacher.process_request("इंटरनेट पर सर्च करो कि आज क्या न्यूज है।"))
    
    # 3. विशाल डेटा स्ट्रीमिंग टेस्ट
    print("\n👤 USER: [स्ट्रीमिंग 1000 पन्नों की किताब...]")
    print(teacher.process_request("आसमान नीला है. पानी गीला होता है. आसमान नीला है."))
    print(f"📊 Memory Status: {memory.memory_stats()}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_test()
