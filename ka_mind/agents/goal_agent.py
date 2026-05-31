"""
Goal Agent - बड़े लक्ष्यों को प्लान में तोड़ना और एग्जीक्यूट करना।
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
import time

class GoalAgent:
    def __init__(self, memory_graph, web_agent, neocortex):
        self.memory = memory_graph
        self.web_agent = web_agent
        self.neocortex = neocortex

    def create_plan(self, goal: str) -> list:
        """लक्ष्य को छोटे स्टेप्स में तोड़ना"""
        print(f"🎯 [Goal Set]: '{goal}'")
        # (भविष्य में इसे LLM से जनरेट करेंगे, अभी बेसिक लॉजिक है)
        plan = [
            f"Step 1: '{goal}' के बारे में मेमोरी ग्राफ में जानकारी खोजें।",
            f"Step 2: अगर जानकारी कम है, तो इंटरनेट (Web Agent) से सर्च करें।",
            f"Step 3: Neocortex से लॉजिक (Reasoning) लगवाकर फाइनल निष्कर्ष निकालें।",
            f"Step 4: सीखे गए नए ज्ञान को 'Improvement' के तौर पर सेव करें।"
        ]
        return plan

    def execute_plan(self, goal: str):
        """प्लान को एक-एक करके रन करना और फीडबैक लूप बनाना"""
        plan = self.create_plan(goal)
        feedback_notes = []
        
        for step in plan:
            print(f"⏳ [Executing]: {step}")
            time.sleep(1) # सिमुलेशन के लिए थोड़ा डिले
            
            if "मेमोरी" in step:
                results = self.memory.search(goal.split()[0])
                if results: feedback_notes.append("✅ मेमोरी में डेटा मिल गया।")
                else: feedback_notes.append("❌ ग्राफ में डेटा नहीं है।")
                
            elif "इंटरनेट" in step and "❌" in feedback_notes[-1]:
                # फीडबैक लूप: अगर मेमोरी में नहीं मिला, तो इंटरनेट से लाओ!
                self.web_agent.search_and_learn(goal)
                feedback_notes.append("✅ इंटरनेट से नया डेटा सीख लिया।")
                
            elif "Neocortex" in step:
                self.neocortex.think_and_reason()
                feedback_notes.append("✅ सोच-समझकर निष्कर्ष निकाल लिया।")
                
            elif "Improvement" in step:
                # खुद का फीडबैक ग्राफ में सेव करना
                atom = KnowledgeAtom(AtomType.FACT, {"text": f"मैंने '{goal}' का टास्क सफलतापूर्वक पूरा किया।"}, category="system_feedback")
                self.memory.add_atom(atom)
                
        print(f"\n🏆 [Task Completed]: '{goal}' पूरी तरह से एग्जीक्यूट हो गया!")
        print(f"📈 [Feedback Loop]: {feedback_notes[-1]}")
