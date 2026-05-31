"""
Memory Ranker - तय करना कि कौन सा Atom कितना ज़रूरी है (Long-term vs Short-term)
"""
class MemoryRanker:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def rank_memories(self):
        """Atoms को Evidence और Usage के आधार पर रैंक करना"""
        for atom_id, atom in self.memory.graph.items():
            # 1. Evidence Score: कितनी बार यह इस्तेमाल हुआ
            evidence_score = atom.usage_count * 0.1
            
            # 2. Confidence Update
            atom.confidence = min(1.0, atom.confidence + evidence_score)
            
            # 3. Memory Tagging
            if atom.confidence >= 0.8:
                atom.memory_type = "Long-term (Strong)"
            elif atom.confidence >= 0.4:
                atom.memory_type = "Short-term (Active)"
            else:
                atom.memory_type = "Temporary (Weak)"
                
        return "🧠 [Memory Ranking]: सभी Atoms को Evidence के आधार पर लॉन्ग-टर्म और शॉर्ट-टर्म में बांट दिया गया है।"
