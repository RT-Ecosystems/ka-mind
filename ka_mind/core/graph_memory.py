"""
Graph Memory - Updated with Privacy Search Filter.
"""
class GraphMemory:
    def __init__(self):
        self.graph = {}

    def add_atom(self, atom) -> bool:
        """नए ज्ञान को जोड़ना (रीयल-टाइम लर्निंग)"""
        if atom.atom_id in self.graph:
            self.graph[atom.atom_id].usage_count += 1
            return False # पहले से पता है
        self.graph[atom.atom_id] = atom
        return True # नया ज्ञान सीखा!

    def search(self, keyword: str, current_user_id: str = "system") -> list:
        """
        सर्च करते समय सिर्फ Public डेटा और Current User का Private डेटा ही लाएगा।
        """
        results = []
        for atom in self.graph.values():
            text = str(atom.content).lower()
            if keyword.lower() in text:
                # Privacy Check (The Lock 🔒)
                if atom.scope == "public" or atom.user_id == current_user_id:
                    results.append(atom)
        return results

    def memory_stats(self):
        public_count = sum(1 for a in self.graph.values() if a.scope == "public")
        private_count = sum(1 for a in self.graph.values() if a.scope == "private")
        return f"Total: {len(self.graph)} Atoms (Public: {public_count}, Private: {private_count})"
