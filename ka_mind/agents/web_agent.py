# KA-Mind Web Agent — Internet search + learn
import urllib.request, urllib.parse, json
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class WebAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def search_and_learn(self, query: str) -> str:
        try:
            enc = urllib.parse.quote(query)
            url = f'https://api.duckduckgo.com/?q={enc}&format=json&no_html=1'
            req = urllib.request.Request(url,
                headers={'User-Agent': 'KA-Mind/2.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            text = data.get('AbstractText', '')
            if text:
                atom = KnowledgeAtom(AtomType.FACT,
                    {'text': text, 'source': 'web', 'query': query},
                    0.75, 'web_search')
                self.memory.add_atom(atom)
                return f'Learned from web: {text[:200]}'
            return 'No web results found.'
        except Exception as e:
            return f'Web search failed: {e}'

    def read_url(self, url: str) -> str:
        try:
            import re
            req = urllib.request.Request(url,
                headers={'User-Agent': 'Mozilla/5.0 KA-Mind/2.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                html = r.read().decode('utf-8', errors='ignore')
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>',  '', html, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()[:5000]
            atom = KnowledgeAtom(AtomType.FACT,
                {'text': text[:500], 'url': url}, 0.70, 'url_read')
            self.memory.add_atom(atom)
            return text
        except Exception as e:
            return f'URL read failed: {e}'
