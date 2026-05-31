"""
Cognitive Generator - जो टीचर के नियमों को पढ़कर सुरक्षित आउटपुट बनाएगा।
"""
from ka_mind.core.knowledge_atom import AtomType

class CognitiveGenerator:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def check_safety(self, task: str) -> bool:
        """आउटपुट बनाने से पहले सेफ्टी चेक (Safety Firewall)"""
        safety_rules = [a.content.get("text") for a in self.memory.graph.values() if a.content.get("skill") == "safety_rules"]
        
        # अगर टास्क में कुछ खतरनाक शब्द हैं
        dangerous_keywords = ["hack", "malware", "virus", "attack", "steal", "नुकसान", "हैक"]
        
        for word in dangerous_keywords:
            if word in task.lower():
                print(f"\n🚨 [SAFETY ALERT]: '{task}' के लिए अनुरोध ब्लॉक कर दिया गया है!")
                for rule in safety_rules:
                    if "हमला" in rule or "नुकसान" in rule:
                        print(f"🛡️ [AI Ethics Firewall]: {rule}")
                return False
        return True

    def generate(self, task: str, skill_type: str) -> str:
        """सुरक्षित रूप से आउटपुट बनाना"""
        # 1. पहले सुरक्षा की जांच करो!
        if not self.check_safety(task):
            return "❌ [Access Denied]: यह अनुरोध मेरी नैतिकता और सुरक्षा नियमों के खिलाफ है।"

        # 2. अगर सुरक्षित है, तो भाषा/कोड जनरेट करो
        skill_rules = [a.content.get("text") for a in self.memory.graph.values() if a.content.get("skill") == skill_type]
        
        output = f"\n--- {task} ---\n"
        output += f"✨ [Applying Rules]: मुझे सिखाए गए {len(skill_rules)} नियमों का पालन करते हुए...\n"
        output += "✅ [Response]: यह कार्य सुरक्षित है। (Here KA-Mind would construct the actual words based on rules.)"
        
        return output
