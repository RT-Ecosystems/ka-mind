# KA-Mind Trainer — Parallel + NeuraBrain Teacher
# BUG FIXED: Now uses 3-layer NeuraBrain Teacher (not raw sentence split)
import os, concurrent.futures, multiprocessing
from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher


def _worker(args):
    text_chunk, domain = args
    from ka_mind.core.graph_memory import GraphMemory
    from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher
    local_mem = GraphMemory()
    teacher   = NeuraBrainTeacher(local_mem)
    teacher.process_chunk(text_chunk, domain)
    return list(local_mem.graph.values())


class KaTrainer:
    def __init__(self, model):
        self.model       = model
        self.chk_dir     = f'./checkpoints/{model.name.lower()}'
        os.makedirs(self.chk_dir, exist_ok=True)
        self.cpu_cores   = max(1, multiprocessing.cpu_count() - 1)

    def train_parallel(self, file_path: str, chunk_size: int = 50000):
        if not os.path.exists(file_path):
            print(f'File not found: {file_path}'); return
        print(f'Parallel training: {self.cpu_cores+1} CPU cores')
        chunks = []
        buf = ''
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                buf += line
                if len(buf) >= chunk_size:
                    chunks.append((buf, self.model.domain))
                    buf = ''
        if buf: chunks.append((buf, self.model.domain))
        print(f'{len(chunks)} chunks created. Processing...')
        added = 0
        with concurrent.futures.ProcessPoolExecutor(
                max_workers=self.cpu_cores) as ex:
            for atom_list in ex.map(_worker, chunks):
                for atom in atom_list:
                    if self.model.memory.add_atom(atom):
                        added += 1
        print(f'Parallel training done: {added:,} atoms added')
        return added

    def save_checkpoint(self) -> str:
        path = os.path.join(self.chk_dir, 'checkpoint.kamind')
        self.model.save(self.chk_dir)
        return path

    def train(self, text: str) -> int:
        """Simple single-thread training on a text string."""
        from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher
        teacher = NeuraBrainTeacher(self.model.memory)
        return teacher.process_chunk(text, self.model.domain)
