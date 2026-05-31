# KA-Mind File Agent — Read and learn from files
import os
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class FileAgent:
    SUPPORTED = ['.txt','.md','.csv','.json','.py','.pdf','.docx']

    def __init__(self, memory_graph, teacher=None):
        self.memory  = memory_graph
        self.teacher = teacher

    def read_and_learn(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f'File not found: {file_path}'
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED:
            return f'Unsupported format: {ext}. Use: {self.SUPPORTED}'
        text = self._read(file_path, ext)
        if not text:
            return 'Could not read file.'
        if self.teacher:
            n = self.teacher.process_chunk(text, 'file', 'system')
            return f'Learned {n} atoms from {os.path.basename(file_path)}'
        atom = KnowledgeAtom(AtomType.FACT,
            {'text': text[:2000], 'file': file_path}, 0.85, 'file')
        self.memory.add_atom(atom)
        return f'Stored content from {os.path.basename(file_path)}'

    def _read(self, path: str, ext: str) -> str:
        if ext in ('.txt','.md','.py'):
            return open(path,'r',encoding='utf-8',errors='ignore').read()
        if ext == '.csv':
            try:
                import csv
                rows = list(csv.reader(open(path,encoding='utf-8',errors='ignore')))
                return '\n'.join([', '.join(r) for r in rows[:200]])
            except: return open(path,'r',errors='ignore').read()
        if ext == '.json':
            import json
            try:
                data = json.load(open(path,encoding='utf-8',errors='ignore'))
                return json.dumps(data, indent=2, ensure_ascii=False)[:5000]
            except: return open(path,'r',errors='ignore').read()
        if ext == '.pdf':
            try:
                import subprocess
                result = subprocess.run(['pdftotext',path,'-'],
                    capture_output=True,text=True)
                if result.returncode==0: return result.stdout
            except: pass
            return 'PDF reading requires pdftotext. Run: apt install poppler-utils'
        if ext == '.docx':
            try:
                import zipfile, re
                with zipfile.ZipFile(path) as z:
                    xml = z.read('word/document.xml').decode('utf-8')
                return re.sub(r'<[^>]+>',' ',xml)[:5000]
            except: return 'Could not read DOCX.'
        return ''
