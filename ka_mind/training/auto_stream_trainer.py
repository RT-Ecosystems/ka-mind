"""
AutoStreamTrainer — HuggingFace datasets → ka-mind streaming training.
Creates your first "Atom Model" without any manual data preparation.
Usage:
    trainer = AutoStreamTrainer(model)
    trainer.train_from_hf("wikipedia", "20220301.en", max_samples=100000)
    print(model.model_size_str)  # "1.2 Million Atom Model"
"""
import time
from ka_mind.teacher.super_teacher import SuperTeacher
from ka_mind.core.knowledge_atom import AtomType


class AutoStreamTrainer:
    """Stream data from HuggingFace datasets directly into ka-mind."""

    def __init__(self, model):
        self.model = model
        self.teacher = SuperTeacher(model.memory, model.vector_graph)
        self._t0 = None
        self._total_samples = 0
        self._total_atoms = 0

    def train_from_hf(self, dataset_name: str, subset: str = None,
                      split: str = "train", max_samples: int = 100000,
                      streaming: bool = True) -> dict:
        """Train from a HuggingFace dataset with streaming."""
        try:
            from datasets import load_dataset
        except ImportError:
            print("❌ datasets library not installed. Run: pip install datasets")
            return {"error": "datasets not installed"}

        print(f"
{'='*55}")
        print(f"  🚀 AutoStream Training: {dataset_name}")
        print(f"{'='*55}")
        if subset:
            print(f"  📦 Subset: {subset}")
        print(f"  📊 Max samples: {max_samples:,}")
        print(f"  🌊 Streaming: {streaming}")
        print(f"{'='*55}
")

        # Load dataset
        try:
            if subset:
                ds = load_dataset(dataset_name, subset, split=split, streaming=streaming)
            else:
                ds = load_dataset(dataset_name, split=split, streaming=streaming)
        except Exception as e:
            print(f"  ❌ Failed to load dataset: {e}")
            # Try fallback datasets
            fallbacks = [
                ("wikitext", "wikitext-103-v1"),
                ("rotten_tomatoes", None),
                ("imdb", None),
            ]
            for name, sub in fallbacks:
                try:
                    if sub:
                        ds = load_dataset(name, sub, split="train", streaming=True)
                    else:
                        ds = load_dataset(name, split="train", streaming=True)
                    print(f"  ✅ Fallback: {name}")
                    break
                except:
                    continue
            else:
                return {"error": "No dataset available"}

        self._t0 = time.time()
        self._total_samples = 0
        self._total_atoms = 0
        sample_count = 0

        for example in ds:
            if sample_count >= max_samples:
                break

            # Extract text from example
            text = example.get("text") or example.get("content") or example.get("sentence") or ""
            if not text or len(text.strip()) < 20:
                continue

            # Teach through SuperTeacher
            new_atoms = self.teacher.teach(text.strip(), domain="streaming")
            self._total_samples += 1
            self._total_atoms += new_atoms
            sample_count += 1

            # Progress update
            if sample_count % 1000 == 0:
                elapsed = time.time() - self._t0
                speed = sample_count / elapsed if elapsed > 0 else 0
                print(f"  📊 Samples: {sample_count:,} | Atoms: {self._total_atoms:,} | "
                      f"Speed: {speed:.0f} samples/s | Time: {elapsed:.0f}s")

            # Free memory
            del text, example

        return self._summary()

    def train_from_texts(self, texts: list) -> dict:
        """Train from a list of text strings."""
        self._t0 = time.time()
        self._total_samples = 0
        self._total_atoms = 0

        print(f"
{'='*55}")
        print(f"  🚀 Training from {len(texts)} texts")
        print(f"{'='*55}
")

        for i, text in enumerate(texts):
            if not text or len(text.strip()) < 10:
                continue
            new_atoms = self.teacher.teach(text.strip(), domain="custom")
            self._total_samples += 1
            self._total_atoms += new_atoms

            if (i + 1) % 500 == 0:
                elapsed = time.time() - self._t0
                print(f"  📊 {i+1}/{len(texts)} | Atoms: {self._total_atoms:,} | "
                      f"Time: {elapsed:.0f}s")

        return self._summary()

    def train_from_file(self, file_path: str, max_lines: int = None) -> dict:
        """Train from a local text file."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        self._t0 = time.time()
        self._total_samples = 0
        self._total_atoms = 0

        print(f"
{'='*55}")
        print(f"  📁 Training from: {file_path}")
        print(f"{'='*55}
")

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if max_lines and i >= max_lines:
                    break
                line = line.strip()
                if len(line) < 20:
                    continue
                new_atoms = self.teacher.teach(line, domain="file")
                self._total_samples += 1
                self._total_atoms += new_atoms

                if (i + 1) % 1000 == 0:
                    elapsed = time.time() - self._t0
                    print(f"  📊 Line {i+1:,} | Atoms: {self._total_atoms:,} | "
                          f"Time: {elapsed:.0f}s")

        return self._summary()

    def _summary(self) -> dict:
        elapsed = time.time() - self._t0
        print(f"
{'='*55}")
        print(f"  ✅ Training Complete!")
        print(f"{'='*55}")
        print(f"  ⏱️  Time      : {elapsed:.0f}s ({elapsed/60:.1f} min)")
        print(f"  📊 Samples   : {self._total_samples:,}")
        print(f"  🧠 Atoms     : {self._total_atoms:,}")
        print(f"  💾 Model     : {self.model.model_size_str}")
        print(f"  📏 Rules     : {self.model.rule_base.total_rules:,}")
        print(f"  ⚡ Speed     : {self._total_samples/elapsed:.0f} samples/s")
        print(f"{'='*55}")

        return {
            "time": elapsed,
            "samples": self._total_samples,
            "atoms": self._total_atoms,
            "model_size": self.model.model_size_str,
            "rules": self.model.rule_base.total_rules,
            "speed": self._total_samples / elapsed if elapsed > 0 else 0
        }
