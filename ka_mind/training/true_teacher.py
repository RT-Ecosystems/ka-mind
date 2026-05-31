"""
True Teacher - भाषा के नियम, इंसानियत और सुरक्षा (Safety) की ट्रेनिंग।
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class TrueTeacher:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def teach_language_and_conversation(self):
        """इंसान कैसे बात करते हैं, और शब्द कैसे जुड़ते हैं?"""
        print("👨‍🏫 [Teacher]: भाषा, बातचीत और शब्दों के नियम (Linguistics) सिखा रहा हूँ...")
        rules = [
            "Conversation Rule: हमेशा सामने वाले इंसान की बात को सुनो, संदर्भ (context) समझो, और फिर सम्मान के साथ जवाब दो।",
            "Word Prediction Rule: हिंदी भाषा में, विशेषण (Adjective) हमेशा संज्ञा (Noun) से पहले आता है (जैसे: 'काला कुत्ता', 'कुत्ता काला' नहीं)।",
            "Thought Process Rule: जवाब देने से पहले, दिमाग में तथ्यों को तार्किक क्रम (Logical Sequence) में सजाओ।"
        ]
        for rule in rules:
            self.memory.add_atom(KnowledgeAtom(AtomType.RULE, {"text": rule, "skill": "conversation_logic"}))

    def teach_ethics_and_safety(self):
        """सुरक्षा, नैतिकता और एथिकल हैकिंग के नियम (The AI Constitution)"""
        print("🛡️ [Teacher]: सुरक्षा और नैतिकता (Ethics & Safety) के कड़े नियम सिखा रहा हूँ...")
        rules = [
            "Absolute Safety Rule: कभी भी ऐसा कोड या जानकारी मत दो जिससे किसी इंसान, सिस्टम या देश को नुकसान पहुंचे।",
            "Ethical Hacking Rule: हैकिंग की जानकारी का इस्तेमाल केवल 'सुरक्षा खामियों को खोजने (Defense)' के लिए करो, 'हमला (Attack)' करने के लिए कभी नहीं।",
            "Refusal Rule: अगर कोई यूजर गलत काम (जैसे मैलवेयर बनाना) के लिए कहे, तो तुरंत मना कर दो और सुरक्षा के नियम याद दिलाओ।"
        ]
        for rule in rules:
            self.memory.add_atom(KnowledgeAtom(AtomType.RULE, {"text": rule, "skill": "safety_rules", "priority": "CRITICAL"}))

    def teach_coding_mechanics(self):
        """प्रोग्रामिंग के नियम (Basic Syntax)"""
        print("👨‍🏫 [Teacher]: प्रोग्रामिंग के नियम सिखा रहा हूँ...")
        rules = [
            "Code Rule: सुरक्षित कोड लिखने के लिए हमेशा इनपुट वैलिडेशन (Input Validation) का इस्तेमाल करो।"
        ]
        for rule in rules:
            self.memory.add_atom(KnowledgeAtom(AtomType.RULE, {"text": rule, "skill": "coding_generation"}))
