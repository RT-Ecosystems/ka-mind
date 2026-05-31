# KA-Mind Model — Complete AI Brain Instance
# Technique: NeuraBrain | Library: KA-Mind
import pickle, os
from ka_mind.core.graph_memory    import GraphMemory
from ka_mind.core.vector_graph    import VectorGraph
from ka_mind.core.neocortex       import Neocortex
from ka_mind.core.composer        import Composer
from ka_mind.core.world_model     import WorldModel
from ka_mind.core.abstractor      import Abstractor
from ka_mind.teacher.master_teacher import MasterTeacher
from ka_mind.agents.web_agent     import WebAgent
from ka_mind.agents.code_agent    import CodeAgent
from ka_mind.agents.vision_agent  import VisionAgent


class KaModel:
    def __init__(self, name: str, domain: str = 'General'):
        self.name    = name
        self.domain  = domain
        self.version = '2.0'

        # Core memory systems
        self.memory       = GraphMemory()
        self.vector_graph = VectorGraph()  # BUG4 FIXED: now connected!

        # Cognitive systems
        self.neocortex = Neocortex(self.memory)
        self.composer  = Composer(self.memory)
        self.world     = WorldModel(self.memory)
        self.abstractor= Abstractor(self.memory)

        # Agents
        self.web_agent    = WebAgent(self.memory)
        self.code_agent   = CodeAgent()
        self.vision_agent = VisionAgent(self.memory)

        # Teacher (BUG3+BUG4 FIXED: VectorGraph connected)
        self.teacher = MasterTeacher(
            self.memory, self.web_agent, self.code_agent,
            self.vision_agent, self.vector_graph
        )

    def think(self, query: str, user_id: str = 'system') -> str:
        return self.teacher.process_request(query, user_id)

    def learn(self, text: str) -> int:
        from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher
        t = NeuraBrainTeacher(self.memory, self.vector_graph)
        n = t.process_chunk(text, self.domain)
        return n

    def train_file(self, file_path: str, max_gb: float = None):
        from ka_mind.training.stream_trainer import StreamTrainer
        trainer = StreamTrainer(self.memory, self.vector_graph,
                                domain=self.domain)
        trainer.train_from_file(file_path, max_gb)

    def train_drive(self, folder: str, max_gb: float = None):
        from ka_mind.training.stream_trainer import StreamTrainer
        trainer = StreamTrainer(self.memory, self.vector_graph,
                                domain=self.domain)
        trainer.train_from_drive(folder, max_gb)

    def deep_sleep(self):
        self.neocortex.run_deep_sleep_cycle()
        self.abstractor.create_concepts()
        self.world.discover_rules()

    def stats(self) -> dict:
        return {'name': self.name, 'domain': self.domain,
                'atoms': len(self.memory.graph),
                'vector_atoms': len(self.vector_graph.graph),
                'edges': sum(len(e) for e in self.memory.edges.values()),
                'memory': self.memory.memory_stats()}

    def save(self, export_dir: str = './models') -> str:
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir,
                            f'{self.name.lower()}_v{self.version}.kamind')
        with open(path, 'wb') as f:
            pickle.dump({'name': self.name, 'domain': self.domain,
                         'memory_graph': self.memory.graph,
                         'edges': self.memory.edges,
                         'version': self.version}, f)
        sz = os.path.getsize(path) / 1024 / 1024
        print(f'Saved: {path} ({sz:.1f} MB)')
        return path

    @classmethod
    def load(cls, filepath: str):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        instance = cls(name=data['name'], domain=data.get('domain','General'))
        instance.memory.graph = data['memory_graph']
        instance.memory.edges = data.get('edges', {})
        instance.version = data.get('version', '2.0')
        print(f'Loaded: {len(instance.memory.graph):,} atoms')
        return instance

    def __repr__(self):
        return (f'KaModel({self.name} v{self.version} | '
                f'atoms={len(self.memory.graph):,} | '
                f'domain={self.domain})')
