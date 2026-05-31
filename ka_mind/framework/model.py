"""
KaModel - KA-Mind तकनीक पर आधारित एक स्वतंत्र मॉडल (Brain Instance)।
"""
import pickle
import os
from ka_mind.core.graph_memory import GraphMemory
from ka_mind.teacher.master_teacher import MasterTeacher
from ka_mind.agents.web_agent import WebAgent
from ka_mind.agents.code_agent import CodeAgent
from ka_mind.agents.vision_agent import VisionAgent

class KaModel:
    def __init__(self, name: str, domain: str = "General"):
        self.name = name
        self.domain = domain
        self.version = "1.0"
        
        self.memory = GraphMemory()
        self.web_agent = WebAgent(self.memory)
        self.code_agent = CodeAgent()
        self.vision_agent = VisionAgent(self.memory)
        
        self.teacher = MasterTeacher(self.memory, self.web_agent, self.code_agent, self.vision_agent)
        
    def think(self, query: str) -> str:
        return self.teacher.process_request(query)

    def save(self, export_dir: str = "./models"):
        os.makedirs(export_dir, exist_ok=True)
        file_path = os.path.join(export_dir, f"{self.name.lower()}_v{self.version}.kamind")
        
        with open(file_path, "wb") as f:
            pickle.dump({
                "name": self.name,
                "domain": self.domain,
                "memory_graph": self.memory.graph
            }, f)
        return file_path

    @classmethod
    def load(cls, filepath: str):
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            
        instance = cls(name=data["name"], domain=data["domain"])
        instance.memory.graph = data["memory_graph"]
        return instance
