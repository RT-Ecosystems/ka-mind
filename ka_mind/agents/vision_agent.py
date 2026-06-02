# KA-Mind Vision Agent v2.0 — HD Image Generation
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class VisionAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph
        self._sd_pipe = None  # Lazy-loaded Stable Diffusion

    def generate_image(self, prompt: str, output: str = 'output.png',
                        use_hd: bool = False) -> str:
        """Generate image from text. Use use_hd=True for Stable Diffusion HD."""
        if use_hd:
            return self._hd_generate(prompt, output)
        return self._simple_generate(prompt, output)

    def _simple_generate(self, prompt: str, output: str) -> str:
        try:
            from PIL import Image, ImageDraw
            import hashlib
            hx = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
            r, g, b = (hx >> 16) & 0xFF, (hx >> 8) & 0xFF, hx & 0xFF
            img = Image.new('RGB', (512, 512), (r, g, b))
            draw = ImageDraw.Draw(img)
            draw.text((20, 240), prompt[:50], fill=(255, 255, 255))
            img.save(output)
            return f'Simple image saved: {output}'
        except ImportError:
            return 'Pillow not installed. Run: pip install Pillow'

    def _hd_generate(self, prompt: str, output: str) -> str:
        """HD image generation using Stable Diffusion."""
        try:
            from diffusers import StableDiffusionPipeline
            import torch

            if self._sd_pipe is None:
                print("Loading Stable Diffusion (first time only)...")
                self._sd_pipe = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                if torch.cuda.is_available():
                    self._sd_pipe = self._sd_pipe.to("cuda")
                print("Stable Diffusion ready!")

            image = self._sd_pipe(prompt, num_inference_steps=25).images[0]
            image.save(output)
            return f'HD image saved: {output}'
        except ImportError:
            return 'diffusers not installed. Run: pip install diffusers torch'
        except Exception as e:
            return f'HD generation failed: {e}. Falling back to simple mode.\n' + self._simple_generate(prompt, output)

    def describe_image(self, path: str) -> str:
        try:
            from PIL import Image
            img = Image.open(path)
            return f'Image: {img.size[0]}x{img.size[1]}, mode={img.mode}'
        except ImportError:
            return 'Pillow not installed.'
        except Exception as e:
            return f'Could not read image: {e}'
