"""
World Model - नियमों की खोज और 'What-If' Simulation.
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class WorldModel:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def discover_rules(self) -> list:
        """फैक्ट्स के आधार पर दुनिया के नियम (Rules) खोजना"""
        rules_found = []
        # (यह बहुत बेसिक है, हम इसे आगे AI NLP से जोड़ेंगे)
        for atom in self.memory.graph.values():
            text = atom.content.get("text", "").lower()
            if "हमेशा" in text or "कभी नहीं" in text:
                rule_atom = KnowledgeAtom(
                    atom_type=AtomType.RULE,
                    content={"rule": text},
                    confidence=0.9,
                    category="world_rule"
                )
                if self.memory.add_atom(rule_atom):
                    rules_found.append(f"📜 [Rule Discovery]: नया नियम खोजा गया -> '{text}'")
        return rules_found

    def simulate_what_if(self, scenario: str) -> str:
        """अगर ऐसा हुआ तो क्या होगा? (Simulation)"""
        # ग्राफ में मौजूद रूल्स के आधार पर परिणाम सोचना
        rules = [a.content.get("rule") for a in self.memory.graph.values() if a.atom_type == AtomType.RULE]
        
        if not rules:
            return "💭 [Simulation Failed]: मेरे पास अभी दुनिया के पर्याप्त नियम (Rules) नहीं हैं।"
            
        return f"🔮 [Simulation Analysis]: '{scenario}' के लिए... मेरे नियमों के अनुसार यह संभावित परिणाम हो सकता है (Based on {len(rules)} rules)."
