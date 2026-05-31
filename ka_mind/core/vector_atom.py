"""
Vector Atom - टेक्स्ट के साथ-साथ ज्ञान को Universal Numbers में सेव करना।
"""
import hashlib
from sentence_transformers import SentenceTransformer

class VectorAtom:
    # हम 50+ भाषाओं को समझने वाला एक लाइटवेट मॉडल लोड करेंगे
    print("🌍 [Universal Encoder]: Multilingual AI लोड हो रहा है...")
    encoder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def __init__(self, text: str, category: str = "general"):
        self.text = text
        self.category = category
        
        # 1. टेक्स्ट को Universal Numbers (Vector) में बदलना
        self.vector = self.encoder.encode(text).tolist()
        
        # 2. Vector के आधार पर ID बनाना (ताकि अलग भाषा का समान अर्थ एक ही ID बनाए!)
        # (सरलता के लिए अभी हम टेक्स्ट का इस्तेमाल कर रहे हैं, असली में वेक्टर हैश होगा)
        s = self.text.lower()
        self.atom_id = hashlib.md5(s.encode()).hexdigest()[:12]

    def get_universal_meaning(self):
        """यह नंबरों की वो सीरीज़ है जिसे इमेज जनरेटर या कोई भी भाषा डिकोडर समझ सकता है"""
        # आउटपुट बहुत बड़ा होगा (384 numbers), इसलिए सिर्फ पहले 5 दिखा रहे हैं
        return [round(num, 4) for num in self.vector[:5]]
