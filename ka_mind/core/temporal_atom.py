"""
Temporal Atom - हर ज्ञान के साथ एक 'Timestamp' और 'Validity' जोड़ना।
"""
import hashlib
import json
from datetime import datetime

class TemporalAtom:
    def __init__(self, text: str, year: int = None, is_current: bool = True):
        self.text = text
        # अगर साल नहीं बताया गया है, तो आज का साल ले लो
        self.year = year if year else datetime.now().year
        self.is_current = is_current # क्या यह बात आज भी सच है?
        
        s = self.text + str(self.year)
        self.atom_id = hashlib.md5(s.encode()).hexdigest()[:12]

    def to_dict(self):
        return {"id": self.atom_id, "text": self.text, "year": self.year, "is_current": self.is_current}
