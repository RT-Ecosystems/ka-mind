# KA-Mind Model v2.1 — All agents wired
import pickle, os, re
from ka_mind.core.graph_memory    import GraphMemory
from ka_mind.core.vector_graph    import VectorGraph
from ka_mind.core.neocortex       import Neocortex
from ka_mind.core.composer        import Composer
from ka_mind.core.world_model     import WorldModel
from ka_mind.core.abstractor      import Abstractor
from ka_mind.agents.web_agent     import WebAgent
from ka_mind.agents.code_agent    import CodeAgent
from ka_mind.agents.vision_agent  import VisionAgent
from ka_mind.agents.math_agent    import MathAgent
from ka_mind.agents.file_agent    import FileAgent
from ka_mind.agents.memory_agent  import MemoryAgent
from ka_mind.agents.translator_agent import TranslatorAgent
from ka_mind.agents.time_agent    import TimeAgent
from ka_mind.teacher.master_teacher import MasterTeacher


class KaModel:
    def __init__(self, name: str, domain: str = 'General'):
        self.name    = name
        self.domain  = domain
        self.version = '2.1'
        self.memory       = GraphMemory()
        self.vector_graph = VectorGraph()
        self.neocortex    = Neocortex(self.memory)
        self.composer     = Composer(self.memory)
        self.world        = WorldModel(self.memory)
        self.abstractor   = Abstractor(self.memory)
        # All agents
        self.web        = WebAgent(self.memory)
        self.code       = CodeAgent()
        self.vision     = VisionAgent(self.memory)
        self.math       = MathAgent(self.memory)
        self.file_agent = FileAgent(self.memory)
        self.mem_agent  = MemoryAgent(self.memory)
        self.translator = TranslatorAgent()
        self.time       = TimeAgent()
        # Master teacher wires everything
        self.teacher = MasterTeacher(
            self.memory, self.web, self.code, self.vision,
            self.vector_graph, self.math, self.file_agent,
            self.mem_agent, self.translator, self.time
        )
        print(f'KaModel {name} v{self.version} ready | domain={domain}')

    def think(self, query: str, user_id: str = 'system') -> str:
        return self.teacher.process_request(query, user_id)

    def learn(self, text: str) -> int:
        from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher
        t = NeuraBrainTeacher(self.memory, self.vector_graph)
        n = t.process_chunk(text, self.domain)
        return n

    def train_file(self, path: str, max_gb: float = None):
        from ka_mind.training.stream_trainer import StreamTrainer
        StreamTrainer(self.memory, self.vector_graph,
                      domain=self.domain).train_from_file(path, max_gb)

    def train_drive(self, folder: str, max_gb: float = None):
        from ka_mind.training.stream_trainer import StreamTrainer
        StreamTrainer(self.memory, self.vector_graph,
                      domain=self.domain).train_from_drive(folder, max_gb)

    def deep_sleep(self):
        print('Running deep sleep cycle...')
        self.neocortex.run_deep_sleep_cycle()
        self.abstractor.create_concepts()
        self.world.discover_rules()
        print('Deep sleep done.')

    def stats(self) -> dict:
        return {'name':self.name,'version':self.version,
                'domain':self.domain,
                'atoms':len(self.memory.graph),
                'vector_atoms':len(self.vector_graph.graph),
                'edges':sum(len(e) for e in self.memory.edges.values()),
                'memory':self.memory.memory_stats()}

    def save(self, path: str = './models') -> str:
        os.makedirs(path, exist_ok=True)
        fp = os.path.join(path, f'{self.name.lower()}_v{self.version}.kamind')
        with open(fp,'wb') as f:
            pickle.dump({'name':self.name,'domain':self.domain,
                         'graph':self.memory.graph,
                         'edges':self.memory.edges,
                         'version':self.version}, f)
        sz = os.path.getsize(fp)/1024/1024
        print(f'Saved: {fp} ({sz:.1f} MB)')
        return fp

    @classmethod
    def load(cls, filepath: str):
        with open(filepath,'rb') as f:
            d = pickle.load(f)
        m = cls(d['name'], d.get('domain','General'))
        m.memory.graph = d['graph']
        m.memory.edges = d.get('edges',{})
        print(f'Loaded: {len(m.memory.graph):,} atoms')
        return m

    def __repr__(self):
        return (f'KaModel({self.name} v{self.version} | '
                f'atoms={len(self.memory.graph):,} | domain={self.domain})')
