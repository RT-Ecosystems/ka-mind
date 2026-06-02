# KA-Mind Stream Trainer v2.4 — mmap for large files
import os, time, mmap
from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher


class StreamTrainer:
    def __init__(self, graph_memory, vector_graph=None,
                 chunk_size_mb: int = 100, domain: str = 'general'):
        self.teacher    = NeuraBrainTeacher(graph_memory, vector_graph)
        self.chunk_size = chunk_size_mb * 1024 * 1024
        self.domain     = domain
        self._t0 = self._bytes = self._chunks = self._atoms = 0

    def train_from_file(self, file_path: str, max_gb: float = None):
        if not os.path.exists(file_path):
            print(f'File not found: {file_path}'); return
        file_size = os.path.getsize(file_path)
        print(f'Streaming training: {file_path} ({file_size/1024**3:.2f} GB)')
        self._t0 = time.time()
        max_bytes = int(max_gb * 1024**3) if max_gb else None
        buf = ''
        # Use mmap for large files
        if file_size > 10 * 1024 * 1024:  # > 10 MB
            with open(file_path, 'r+b') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    for line in iter(mm.readline, b''):
                        try:
                            line_str = line.decode('utf-8', errors='ignore')
                        except:
                            continue
                        buf += line_str
                        self._bytes += len(line_str.encode('utf-8'))
                        if max_bytes and self._bytes >= max_bytes:
                            self._process(buf); break
                        if len(buf.encode('utf-8')) >= self.chunk_size:
                            self._process(buf)
                            buf = ''
                    if buf.strip() and (not max_bytes or self._bytes < max_bytes):
                        self._process(buf)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    buf += line
                    self._bytes += len(line.encode('utf-8'))
                    if max_bytes and self._bytes >= max_bytes:
                        self._process(buf); break
                    if len(buf.encode('utf-8')) >= self.chunk_size:
                        self._process(buf)
                        buf = ''
                if buf.strip():
                    self._process(buf)
        self._summary()

    def train_from_drive(self, folder: str, max_gb: float = None):
        try:
            from google.colab import drive
            drive.mount('/content/drive')
        except ImportError:
            pass
        root = '/content/drive/MyDrive'
        path = os.path.join(root, folder)
        if not os.path.exists(path): path = folder
        exts = ('.txt', '.md', '.json', '.csv', '.py')
        self._t0 = time.time()
        max_bytes = int(max_gb * 1024**3) if max_gb else None
        buf = ''
        for root_d, _, files in os.walk(path):
            for fn in files:
                if not any(fn.endswith(e) for e in exts): continue
                try:
                    content = open(os.path.join(root_d, fn),
                                   'r', encoding='utf-8', errors='ignore').read()
                    buf += content + '
'
                    self._bytes += len(content.encode('utf-8'))
                except Exception: pass
                if max_bytes and self._bytes >= max_bytes: break
                if len(buf.encode('utf-8')) >= self.chunk_size:
                    self._process(buf); buf = ''
            if max_bytes and self._bytes >= max_bytes: break
        if buf.strip(): self._process(buf)
        self._summary()

    def train_from_texts(self, texts: list):
        self._t0 = time.time()
        for text in texts:
            self._process(text)
        self._summary()

    def _process(self, text: str):
        new_atoms = self.teacher.process_chunk(text, self.domain)
        self._chunks += 1
        self._atoms  += new_atoms
        del text
        if self._chunks % 10 == 0:
            el = time.time() - self._t0
            gb = self._bytes / 1024**3
            sp = self._bytes / el / 1024**2 if el > 0 else 0
            print(f'  chunk={self._chunks:4d} | {gb:.3f}GB | {sp:.1f}MB/s | atoms={self._atoms:,}')

    def _summary(self):
        el = time.time() - self._t0
        gb = self._bytes / 1024**3
        print(f'\nTraining complete!')
        print(f'  Time  : {el/3600:.2f}h ({el:.0f}s)')
        print(f'  Data  : {gb:.3f} GB')
        print(f'  Atoms : {self._atoms:,}')
        if el > 0: print(f'  Speed : {gb*1024/el*60:.1f} GB/hour')
