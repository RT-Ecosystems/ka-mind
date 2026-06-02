# KA-Mind Model v2.3 — Reasoning Engine integrated
import pickle, os, re
from ka_mind.core.graph_memory       import GraphMemory
from ka_mind.core.vector_graph       import VectorGraph
from ka_mind.core.neocortex          import Neocortex
from ka_mind.core.reasoning_engine   import ReasoningEngine
from ka_mind.core.composer           import Composer
from ka_mind.core.world_model        import WorldModel
from ka_mind.core.knowledge_pack     import KnowledgePack
from ka_mind.core.inference_cache   import InferenceCache
from ka_mind.core.abstractor         import Abstractor
from ka_mind.agents.web_agent        import WebAgent
from ka_mind.agents.code_agent       import CodeAgent
from ka_mind.agents.vision_agent     import VisionAgent
from ka_mind.agents.math_agent       import MathAgent
from ka_mind.agents.file_agent       import FileAgent
from ka_mind.agents.memory_agent     import MemoryAgent
from ka_mind.agents.translator_agent import TranslatorAgent
from ka_mind.agents.time_agent       import TimeAgent
from ka_mind.agents.api_connector_agent import APIConnectorAgent
from ka_mind.teacher.master_teacher  import MasterTeacher
from ka_mind.teacher.super_teacher   import SuperTeacher


class KaModel:
    def __init__(self, name: str, domain: str = 'General'):
        self.name     = name
        self.domain   = domain
        self.version  = '2.3'
        self.memory       = GraphMemory()
        self.vector_graph = VectorGraph()
        self.cache = InferenceCache()
        self.neocortex    = Neocortex(self.memory)
        self.reasoner     = ReasoningEngine(self.memory)
        self.composer     = Composer(self.memory)
        self.world        = WorldModel(self.memory)
        self.abstractor   = Abstractor(self.memory)
        self.web        = WebAgent(self.memory)
        self.code       = CodeAgent()  # CodeAgent v3.0
        self.vision     = VisionAgent(self.memory)
        self.math       = MathAgent(self.memory)
        self.file_agent = FileAgent(self.memory)
        self.mem_agent  = MemoryAgent(self.memory)
        self.translator = TranslatorAgent()
        self.time       = TimeAgent()
        self.api        = APIConnectorAgent(self.memory)
        self.teacher    = MasterTeacher(
            self.memory, self.web, self.code, self.vision,
            self.vector_graph, self.math, self.file_agent,
            self.mem_agent, self.translator, self.time,
            api_agent=self.api
        )
        print(f'KaModel {name} v{self.version} | domain={domain} | 10 agents | reasoning active')

    def think(self, q: str, user_id: str = 'system') -> str:
        cached = self.cache.get(q)
        if cached:
            return cached
        answer = self.teacher.process_request(q, user_id)
        self.cache.set(q, answer)
        return answer

    def reason(self, query: str) -> str:
        return self.reasoner.reason(query)

    def why(self, observation: str) -> list:
        return self.reasoner.abduction(observation)

    def connect_api(self, api_key: str, api_name: str = None) -> str:
        return self.api.add_api(api_key, api_name)

    def use_github(self, command: str) -> str:
        return self.api.use_github(command)

    def learn(self, text: str, use_super: bool = True) -> int:
        if use_super:
            return self.super_teacher.teach(text, self.domain)
        else:
        from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher
        t = NeuraBrainTeacher(self.memory, self.vector_graph)
        n = t.process_chunk(text, self.domain)
        return n

    def train_file(self, path: str, max_gb: float = None):
        from ka_mind.training.stream_trainer import StreamTrainer
from ka_mind.training.auto_stream_trainer import AutoStreamTrainer
        StreamTrainer(self.memory, self.vector_graph,
                      domain=self.domain).train_from_file(path, max_gb)

    def train_drive(self, folder: str, max_gb: float = None):
        from ka_mind.training.stream_trainer import StreamTrainer
from ka_mind.training.auto_stream_trainer import AutoStreamTrainer
        StreamTrainer(self.memory, self.vector_graph,
                      domain=self.domain).train_from_drive(folder, max_gb)

    
    def train_hf(self, dataset: str, subset: str = None,
                 max_samples: int = 100000) -> dict:
        """Train from HuggingFace dataset with streaming."""
        trainer = AutoStreamTrainer(self)
        return trainer.train_from_hf(dataset, subset, max_samples=max_samples)

    def load_knowledge_packs(self) -> int:
        """Load pre-built general knowledge."""
        return KnowledgePack.load_all(self.memory)

    def deep_sleep(self):
        self.neocortex.run_deep_sleep_cycle()
        self.abstractor.create_concepts()
        self.world.discover_rules()

    
    @property
    def atom_count(self) -> int:
        """Total Knowledge Atoms in the model (like parameter count in LLMs)."""
        return len(self.memory.graph)

    @property
    def model_size_str(self) -> str:
        """Human-readable model size."""
        count = self.atom_count
        if count >= 1_000_000_000:
            return f"{count/1_000_000_000:.1f} Billion Atom Model"
        elif count >= 1_000_000:
            return f"{count/1_000_000:.1f} Million Atom Model"
        elif count >= 1_000:
            return f"{count/1_000:,} Atom Model"
        return f"{count} Atom Model"

    def stats(self) -> dict:
        return {'name': self.name, 'version': self.version,
                'domain': self.domain,
                'atoms': len(self.memory.graph),
                'vector_atoms': len(self.vector_graph.graph),
                'connected_apis': list(self.api.registered.keys()),
                'memory': self.memory.memory_stats()}

    def save(self, path: str = './models') -> str:
        os.makedirs(path, exist_ok=True)
        fp = os.path.join(path, f'{self.name.lower()}_v{self.version}.kamind')
        with open(fp, 'wb') as f:
            pickle.dump({'name': self.name, 'domain': self.domain,
                         'graph': self.memory.graph,
                         'edges': self.memory.edges,
                         'version': self.version}, f)
        print(f'Saved: {fp} ({os.path.getsize(fp)/1024/1024:.1f} MB) [{self.model_size_str}]')
        return fp

    @classmethod
    def load(cls, filepath: str):
        with open(filepath, 'rb') as f:
            d = pickle.load(f)
        m = cls(d['name'], d.get('domain', 'General'))
        m.memory.graph = d['graph']
        m.memory.edges = d.get('edges', {})
        print(f'Loaded: {len(m.memory.graph):,} atoms')
        return m

    def __repr__(self):
        return (f'KaModel({self.name} v{self.version} | '
                f'atoms={len(self.memory.graph):,} | domain={self.domain})')
