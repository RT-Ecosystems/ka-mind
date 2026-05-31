# KA-Mind Vision Agent — Image understanding and generation
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class VisionAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def generate_image(self, prompt: str, output: str = 'output.png') -> str:
        try:
            from PIL import Image, ImageDraw
            import hashlib
            hx  = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
            r,g,b = (hx>>16)&0xFF, (hx>>8)&0xFF, hx&0xFF
            img  = Image.new('RGB', (512, 512), (r, g, b))
            draw = ImageDraw.Draw(img)
            for i in range(0, 512, 40):
                draw.line([(i,0),(i,512)], fill=(min(r+40,255),g,b))
            for j in range(0, 512, 40):
                draw.line([(0,j),(512,j)], fill=(r,min(g+40,255),b))
            draw.text((20, 240), prompt[:50], fill=(255,255,255))
            img.save(output)
            return f'Image saved: {output}'
        except ImportError:
            return 'Install Pillow: pip install Pillow'

    def describe_image(self, image_path: str) -> str:
        try:
            from ka_mind.core.vector_atom import VectorAtom
            from PIL import Image
            encoder = VectorAtom._get_encoder()
            if encoder:
                return f'Image at {image_path} — use CLIP for full description.'
            return f'Image loaded: {image_path}'
        except Exception as e:
            return f'Vision error: {e}'
