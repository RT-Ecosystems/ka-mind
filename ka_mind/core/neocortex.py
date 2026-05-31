"""
Neocortex - KA-Mind का एडवांस्ड थिंकिंग और रीज़निंग इंजन।
"""
class Neocortex:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def think_and_reason(self) -> list:
        """
        दिमाग में मौजूद Atoms को जोड़कर नया ज्ञान (Self-Generated Knowledge) बनाना।
        """
        thoughts = []
        new_discoveries = 0
        
        # 1. Multi-hop Reasoning (A -> B, B -> C = A -> C)
        # (यह एक बेसिक लॉजिक है जिसे हम भविष्य में और एडवांस करेंगे)
        facts = list(self.memory.graph.values())
        
        for atom1 in facts:
            text1 = atom1.content.get("text", "").lower()
            if " एक " in text1 and " है" in text1: # जैसे: "कौवा एक पक्षी है"
                subject1 = text1.split(" एक ")[0].strip()
                object1 = text1.split(" एक ")[1].replace(" है", "").strip()
                
                for atom2 in facts:
                    text2 = atom2.content.get("text", "").lower()
                    if object1 in text2 and "होते हैं" in text2: # जैसे: "पक्षियों के पंख होते हैं"
                        feature = text2.replace(object1, "").replace("के ", "").replace("होते हैं", "").strip()
                        
                        # नया ज्ञान खुद पैदा करना!
                        new_fact = f"{subject1} के {feature} होते हैं।"
                        thoughts.append(f"💡 [Reasoning]: अगर '{text1}' और '{text2}', तो इसका मतलब -> '{new_fact}'")
                        new_discoveries += 1
                        
        return thoughts

    def detect_contradictions(self) -> list:
        """
        डेटा में टकराव (Contradictions) खोजना।
        """
        alerts = []
        facts = list(self.memory.graph.values())
        
        for i, atom1 in enumerate(facts):
            for atom2 in facts[i+1:]:
                text1 = atom1.content.get("text", "").lower()
                text2 = atom2.content.get("text", "").lower()
                
                # अगर एक वाक्य दूसरे का ठीक उल्टा है (Basic Negation Check)
                if text1 == text2.replace(" नहीं", "") or text2 == text1.replace(" नहीं", ""):
                    atom1.confidence -= 0.5 # दोनों का भरोसा कम कर दो
                    atom2.confidence -= 0.5
                    alerts.append(f"⚠️ [Contradiction Alert]: टकराव मिला! ('{text1}' VS '{text2}') - Confidence घटाया गया।")
                    
        return alerts

    def run_deep_sleep_cycle(self):
        """जब सिस्टम खाली हो, तो यह बैकग्राउंड में सोचकर ग्राफ को साफ और स्मार्ट करेगा"""
        print("\n🧠 [Neocortex Deep Sleep Activated]: सिस्टम खुद से सोच रहा है...")
        
        # 1. Contradictions पकड़ना
        alerts = self.detect_contradictions()
        for alert in alerts: print(alert)
        
        # 2. Reasoning से नया ज्ञान बनाना
        thoughts = self.think_and_reason()
        for thought in thoughts: print(thought)
        
        print("✅ [Neocortex]: डीप स्लीप साइकल पूरी हुई। ग्राफ अब ज्यादा स्मार्ट है!")
