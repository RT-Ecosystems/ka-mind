# KA-Mind Memory Agent — Persistent cross-session memory
import json, os, time
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class MemoryAgent:
    def __init__(self, memory_graph, storage_path='./ka_memory.json'):
        self.memory  = memory_graph
        self.path    = storage_path
        self._load_persistent()

    def remember(self, fact: str, user_id: str = 'system') -> str:
        atom = KnowledgeAtom(AtomType.FACT,
            {'text': fact, 'remembered_at': time.time(),
             'persistent': True}, 0.95, 'memory_agent',
            user_id=user_id)
        self.memory.add_atom(atom)
        self._save_persistent()
        return f'Remembered: {fact[:80]}'

    def recall(self, query: str, user_id: str = 'system') -> str:
        results = self.memory.search_scored(query, user_id, top_k=5)
        memories = [a for a,_ in results
                    if a.content.get('persistent')]
        if not memories:
            return 'No specific memory found for this.'
        return ' | '.join(m.to_text() for m in memories[:3])

    def forget(self, query: str, user_id: str = 'system') -> str:
        results = self.memory.search(query, user_id)
        removed = 0
        for atom in results:
            if atom.content.get('persistent') and atom.user_id==user_id:
                del self.memory.graph[atom.atom_id]
                removed += 1
        if removed: self._save_persistent()
        return f'Forgot {removed} memories about: {query}'

    def _save_persistent(self):
        data = {}
        for aid, atom in self.memory.graph.items():
            if atom.content.get('persistent'):
                data[aid] = atom.to_dict()
        json.dump(data, open(self.path,'w'), indent=2, default=str)

    def _load_persistent(self):
        if not os.path.exists(self.path): return
        try:
            data = json.load(open(self.path))
            for aid, d in data.items():
                from ka_mind.core.knowledge_atom import AtomType
                atom = KnowledgeAtom(
                    AtomType.FACT, d.get('content',{}),
                    d.get('confidence',0.9), 'persistent')
                atom.atom_id = aid
                self.memory.graph[aid] = atom
        except: pass
