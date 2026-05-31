"""
Temporal Reasoner - समय के आधार पर सच और झूठ का फैसला करना।
"""
class TemporalReasoner:
    def __init__(self):
        self.timeline = []

    def add_event(self, atom):
        self.timeline.append(atom)
        # टाइमलाइन को साल के हिसाब से सॉर्ट (Sort) करना
        self.timeline.sort(key=lambda x: x.year)

    def ask_question(self, entity: str, target_year: int = None):
        """किसी भी साल का सच खोजना"""
        results = [a for a in self.timeline if entity.lower() in a.text.lower()]
        
        if not results: return "🤷 [Temporal Logic]: मुझे इसके बारे में कोई जानकारी नहीं है।"
        
        if target_year:
            # उस साल के आस-पास का फैक्ट ढूंढो
            specific_results = [a for a in results if a.year <= target_year]
            if specific_results:
                best_match = specific_results[-1] # उस साल के सबसे करीब वाला सच
                return f"⏳ [वर्ष {target_year} का सच]: {best_match.text}"
            return f"⏳ [{target_year} में]: मुझे इस समय काल का कोई डेटा नहीं मिला।"
            
        else:
            # अगर साल नहीं पूछा, तो सबसे ताज़ा (Current) सच बताओ
            latest_match = results[-1]
            return f"🟢 [वर्तमान सच (Latest)]: {latest_match.text} (Recorded in {latest_match.year})"
