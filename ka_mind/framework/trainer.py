"""
KaTrainer - Updated with Multiprocessing Engine for CPU Parallelism!
"""
import re
import os
import json
import concurrent.futures
import multiprocessing
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

# ग्लोबल वर्कर फंक्शन (ताकि Multiprocessing इसे आसानी से पिक कर सके)
def _process_chunk_worker(args):
    text_chunk, domain_category = args
    sentences = re.split(r'(?<=[.!?]) +', text_chunk)
    local_atoms = []
    
    for sentence in sentences:
        if len(sentence.strip()) > 15:
            atom = KnowledgeAtom(
                atom_type=AtomType.FACT, 
                content={"text": sentence.strip()}, 
                source="parallel_stream", 
                category=domain_category
            )
            local_atoms.append(atom)
    return local_atoms

class KaTrainer:
    def __init__(self, model):
        self.model = model
        self.checkpoint_dir = f"./checkpoints/{self.model.name.lower()}"
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        # CPU कोर्सेस की संख्या पता करना
        self.cpu_cores = max(1, multiprocessing.cpu_count() - 1)

    def train_parallel(self, file_path: str, chunk_size: int = 5000):
        """
        विशाल टेक्स्ट फाइल को कई CPU कोर्सेस पर एक साथ (Parallel) प्रोसेस करना।
        """
        print(f"⚡ [Multiprocessing]: {self.cpu_cores + 1} CPU Cores डिटेक्ट हुए!")
        print(f"🚀 महा-ट्रेनिंग शुरू... (File: {file_path})")
        
        if not os.path.exists(file_path):
            return
            
        atoms_added = 0
        chunks = []
        current_chunk = ""
        
        # 1. फाइल को पढ़ना और चंक्स (Chunks) में तोड़ना
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                current_chunk += line + " "
                if len(current_chunk) >= chunk_size:
                    chunks.append((current_chunk, self.model.domain))
                    current_chunk = ""
        if current_chunk:
            chunks.append((current_chunk, self.model.domain))
            
        print(f"📦 डेटा को {len(chunks)} पैकेट्स में बाँटा गया। प्रोसेसिंग शुरू...")

        # 2. Parallel Processing (जादू यहाँ होता है)
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.cpu_cores) as executor:
            results = executor.map(_process_chunk_worker, chunks)
            
            # 3. सभी CPU कोर्सेस से बने हुए Atoms को मेन मेमोरी ग्राफ में मर्ज करना
            for atom_list in results:
                for atom in atom_list:
                    if self.model.memory.add_atom(atom):
                        atoms_added += 1
                        
        print(f"✅ पैरेलल ट्रेनिंग सफल! {atoms_added} नए Atoms '{self.model.name}' के दिमाग में सेव हो गए।")
        return atoms_added
