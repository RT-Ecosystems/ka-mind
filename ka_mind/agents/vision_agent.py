"""
Vision Agent - KA-Mind की आँखें और कल्पना (Image Generation).
"""
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType

class VisionAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def generate_image(self, prompt: str) -> str:
        thoughts = [f"🎨 [Vision Agent]: '{prompt}' के लिए छवि (Image) की कल्पना कर रहा हूँ..."]
        
        try:
            from PIL import Image, ImageDraw
            import hashlib
            
            # Simple Lightweight Image Generation (बिना GPU के तुरंत काम करेगा)
            hx = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
            r, g, b = (hx>>16)&0xFF, (hx>>8)&0xFF, hx&0xFF
            
            w, h = 512, 512
            img = Image.new("RGB", (w, h), (r, g, b))
            draw = ImageDraw.Draw(img)
            
            # कुछ एब्सट्रैक्ट पैटर्न बनाना
            for i in range(0, w, 40):
                draw.line([(i,0),(i,h)], fill=(min(r+50,255),g,b), width=2)
            for j in range(0, h, 40):
                draw.line([(0,j),(w,j)], fill=(r,min(g+50,255),b), width=2)
                
            draw.text((20, h//2), prompt[:50], fill=(255,255,255))
            
            filename = f"kamind_image_{hx%1000}.png"
            img.save(filename)
            
            # नॉलेज ग्राफ में इमेज का डेटा सेव करना (Multimodal Atom)
            atom = KnowledgeAtom(AtomType.FACT, {"image_prompt": prompt, "file": filename}, category="multimodal")
            self.memory.add_atom(atom)
            
            thoughts.append(f"✅ इमेज सफलतापूर्वक बन गई: {filename}")
            thoughts.append("🧠 [Multimodal Atom] ग्राफ में सेव कर लिया गया।")
            
            return "\n".join(thoughts)
            
        except ImportError:
            return "❌ Pillow लाइब्रेरी इंस्टॉल नहीं है। रन करें: pip install Pillow"
