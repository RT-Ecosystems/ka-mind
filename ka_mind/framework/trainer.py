"""
KaTrainer - Updated with Checkpointing, Auto-Resume, and Deduplication!
"""
import re
import os
import json
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class KaTrainer:
    def __init__(self, model):
        self.model = model
        self.checkpoint_dir = f"./checkpoints/{self.model.name.lower()}"
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def save_checkpoint(self, current_row: int, dataset_name: str):
        """ट्रेनिंग की प्रोग्रेस को सेव करना (ताकि क्रैश होने पर यहीं से शुरू हो)"""
        checkpoint_data = {
            "model_name": self.model.name,
            "last_dataset": dataset_name,
            "last_processed_row": current_row
        }
        
        # 1. प्रोग्रेस सेव करना
        with open(f"{self.checkpoint_dir}/progress.json", "w") as f:
            json.dump(checkpoint_data, f)
            
        # 2. मॉडल का दिमाग (Atoms) सेव करना
        self.model.save(self.checkpoint_dir)
        print(f"💾 [Checkpoint Saved]: Row {current_row} तक का डेटा सुरक्षित कर लिया गया है!")

    def load_checkpoint(self, dataset_name: str) -> int:
        """चेक करना कि क्या कोई पुरानी अधूरी ट्रेनिंग है?"""
        progress_file = f"{self.checkpoint_dir}/progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, "r") as f:
                data = json.load(f)
            if data.get("last_dataset") == dataset_name:
                last_row = data.get("last_processed_row", 0)
                print(f"🔄 [Resume Training]: सर्वर क्रैश रिकवरी! ट्रेनिंग Row {last_row} से वापस शुरू हो रही है...")
                return last_row
        return 0

    def train_from_huggingface(self, dataset_path: str, text_column: str = "text", max_rows: int = 1000):
        try:
            from datasets import load_dataset
        except ImportError:
            return
            
        # पुरानी प्रोग्रेस चेक करना (Resume)
        start_row = self.load_checkpoint(dataset_path)
        
        dataset = load_dataset(dataset_path, split="train", streaming=True)
        
        atoms_added = 0
        merged_duplicates = 0
        current_row = 0
        
        for row in dataset:
            # अगर यह डेटा हम पहले पढ़ चुके हैं, तो स्किप करो (Skip to start_row)
            if current_row < start_row:
                current_row += 1
                continue
                
            if current_row >= start_row + max_rows:
                break
                
            text_data = row.get(text_column, "")
            sentences = re.split(r'(?<=[.!?]) +', text_data)
            
            for sentence in sentences:
                if len(sentence.strip()) > 15:
                    atom = KnowledgeAtom(
                        atom_type=AtomType.FACT, 
                        content={"text": sentence.strip()}, 
                        source=f"HF:{dataset_path}", 
                        category=self.model.domain
                    )
                    
                    # Deduplication Logic (यहाँ ग्राफ खुद डुप्लीकेट को मर्ज करेगा)
                    is_new = self.model.memory.add_atom(atom)
                    if is_new:
                        atoms_added += 1
                    else:
                        merged_duplicates += 1
            
            current_row += 1
            
            # हर 100 लाइन के बाद ऑटो-सेव (Checkpointing)
            if current_row % 100 == 0:
                print(f"  ↳ Processed {current_row} rows | New KAs: {atoms_added} | Merged Duplicates: {merged_duplicates}")
                self.save_checkpoint(current_row, dataset_path)
                
        print(f"✅ ट्रेनिंग सेशन पूरा! {atoms_added} नए ज्ञान जुड़े और {merged_duplicates} पुरानी बातें मजबूत (Merge) हुईं।")
        return atoms_added
