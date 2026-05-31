"""
Web Agent - इंटरनेट से सीखकर ग्राफ में ऑटोमैटिकली सेव करना।
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class WebAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def search_and_learn(self, query: str) -> str:
        """वेब से जानकारी लाना और उसे Public ज्ञान बनाकर हमेशा के लिए याद कर लेना"""
        # डमी सर्च रिजल्ट (असल में यहाँ DuckDuckGo API होगी)
        fake_internet_result = f"इंटरनेट के अनुसार, {query} का जवाब है: 2026 में भारत की GDP लगभग 4 ट्रिलियन डॉलर के पार जा चुकी है।"
        
        # 1. सीखे गए ज्ञान को Atom में बदलना (Scope = Public)
        new_fact = KnowledgeAtom(
            atom_type=AtomType.FACT,
            content={"text": fake_internet_result},
            source="internet_search",
            scope="public",  # यह सबके काम आएगा!
            user_id="system"
        )
        
        # 2. दिमाग में सेव करना (Continuous Learning)
        is_new = self.memory.add_atom(new_fact)
        
        status = "💡 [नया ज्ञान सीखा और दिमाग में सेव कर लिया!]" if is_new else "✅ [यह मुझे पहले से पता था]"
        return f"{status}\n{fake_internet_result}"
