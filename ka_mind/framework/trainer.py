"""
KaTrainer - Updated with Hugging Face Cloud Streaming!
"""
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class KaTrainer:
    def __init__(self, model):
        self.model = model

    def train_from_huggingface(self, dataset_path: str, text_column: str = "text", split: str = "train", max_rows: int = 1000):
        """
        Hugging Face से सीधे डेटा स्ट्रीम करना (No Download, No RAM Crash!)
        """
        try:
            from datasets import load_dataset
        except ImportError:
            print("❌ Error: 'datasets' लाइब्रेरी इंस्टॉल नहीं है। 'pip install datasets' रन करें।")
            return

        print(f"☁️ [Trainer]: Hugging Face से '{dataset_path}' की लाइव स्ट्रीमिंग शुरू... (Limit: {max_rows} rows)")
        
        # जादुई फीचर: streaming=True (यह डेटा को हार्ड डिस्क पर सेव नहीं होने देगा)
        dataset = load_dataset(dataset_path, split=split, streaming=True)
        
        atoms_added = 0
        rows_processed = 0
        
        for row in dataset:
            if rows_processed >= max_rows:
                break
                
            text_data = row.get(text_column, "")
            if not text_data:
                continue
                
            # टेक्स्ट को वाक्यों में तोड़ना और प्रोसेस करना
            sentences = re.split(r'(?<=[.!?]) +', text_data)
            for sentence in sentences:
                if len(sentence.strip()) > 15:
                    atom = KnowledgeAtom(
                        atom_type=AtomType.FACT, 
                        content={"text": sentence.strip()}, 
                        source=f"HF:{dataset_path}", 
                        category=self.model.domain
                    )
                    if self.model.memory.add_atom(atom):
                        atoms_added += 1
            
            rows_processed += 1
            if rows_processed % 100 == 0:
                print(f"  ↳ Processed {rows_processed} rows... ({atoms_added} KAs created)")
                
        print(f"✅ HF ट्रेनिंग पूरी! {atoms_added} नए Atoms '{self.model.name}' के दिमाग में सेव हो गए।")
        return atoms_added
