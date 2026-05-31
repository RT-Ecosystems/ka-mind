"""
KaCompiler - ट्रेनिंग के बाद मॉडल को ऑप्टिमाइज़ और एक्सपोर्ट करना।
"""
import os
import shutil
from ka_mind.framework.model import KaModel

class KaCompiler:
    def __init__(self, checkpoint_path: str):
        self.checkpoint_path = checkpoint_path
        print(f"🛠️ [Compiler]: मॉडल को {checkpoint_path} से लोड किया जा रहा है...")
        self.model = KaModel.load(checkpoint_path)

    def optimize_and_compile(self, output_dir: str = "./releases", version: str = "1.0_final"):
        print("\n🧹 [Optimizer]: मेमोरी ग्राफ की सफाई (Pruning) शुरू...")
        
        initial_atoms = len(self.model.memory.graph)
        atoms_to_delete = []
        
        # 1. Pruning: जो Atoms गलत हैं या बहुत कम यूज़ हुए हैं, उन्हें हटाना
        for atom_id, atom in self.model.memory.graph.items():
            # अगर कॉन्फिडेंस 0.2 से कम है, तो उसे डिलीट की लिस्ट में डालो
            if atom.confidence < 0.2:
                atoms_to_delete.append(atom_id)
                
        for atom_id in atoms_to_delete:
            del self.model.memory.graph[atom_id]
            
        final_atoms = len(self.model.memory.graph)
        print(f"✂️ [Pruning]: {initial_atoms - final_atoms} कमज़ोर Atoms डिलीट किए गए।")
        
        # 2. Compiling: फाइनल प्रोडक्शन फाइल बनाना
        os.makedirs(output_dir, exist_ok=True)
        self.model.version = version
        final_path = self.model.save(output_dir)
        
        # 3. Cleanup: पुराने टेंपरेरी चेकपॉइंट्स डिलीट करना (ऑप्शनल)
        self._cleanup_checkpoints()
        
        print(f"\n✅ [Success]: मॉडल सफलतापूर्वक कंपाइल हो गया!")
        print(f"📦 Production Brain File: {final_path}")
        return final_path

    def _cleanup_checkpoints(self):
        """पुराने चेकपॉइंट फोल्डर को साफ करना ताकि स्पेस बचे"""
        chk_dir = f"./checkpoints/{self.model.name.lower()}"
        if os.path.exists(chk_dir):
            try:
                shutil.rmtree(chk_dir)
                print(f"🗑️ [Cleanup]: पुराने टेंपरेरी चेकपॉइंट्स हटा दिए गए।")
            except Exception as e:
                pass
