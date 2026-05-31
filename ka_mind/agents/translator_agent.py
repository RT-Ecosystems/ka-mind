# KA-Mind Translator Agent — Language translation
import urllib.request, urllib.parse, json


class TranslatorAgent:
    def translate(self, text: str, to_lang: str = 'en',
                  from_lang: str = 'auto') -> str:
        try:
            # MyMemory free API (no key needed)
            encoded = urllib.parse.quote(text[:500])
            lang_pair = f'{from_lang}|{to_lang}'
            url = (f'https://api.mymemory.translated.net/get'
                   f'?q={encoded}&langpair={lang_pair}')
            req = urllib.request.Request(
                url, headers={'User-Agent':'KA-Mind/2.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            result = data.get('responseData',{}).get('translatedText','')
            if result:
                return result
            return f'Translation unavailable for: {text[:50]}'
        except Exception as e:
            return f'Translation failed: {e}'

    def detect_language(self, text: str) -> str:
        hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
        if hindi_chars > len(text) * 0.3: return 'hi'
        return 'en'  # Default assumption
