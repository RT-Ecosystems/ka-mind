# KA-Mind Web Agent — DuckDuckGo + Cache
# FIX: Checks memory cache before calling DDG (no repeated calls!)
import urllib.request, urllib.parse, urllib.error, json, time
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class WebAgent:
    CACHE_HOURS = 6  # Same query not searched again for 6 hours

    def __init__(self, memory_graph):
        self.memory    = memory_graph
        self._call_log = {}  # query -> timestamp

    def search_and_learn(self, query: str) -> str:
        # STEP 1: Check memory cache first (no DDG call needed)
        cached = self._check_cache(query)
        if cached:
            return f'[Memory] {cached}'

        # STEP 2: Rate limit — same query within 6 hours? Skip DDG
        if self._is_rate_limited(query):
            return 'Web search rate limit: same query searched recently.'

        # STEP 3: Call DuckDuckGo
        result = self._ddg_search(query)
        if result:
            self._save_to_memory(query, result)
            self._call_log[query.lower()] = time.time()
            return f'[Web] {result[:300]}'

        return 'No relevant information found online.'

    def _check_cache(self, query: str) -> str:
        qw = set(query.lower().split())
        for atom in self.memory.graph.values():
            if atom.content.get('source') != 'web': continue
            aw = set(atom.to_text().lower().split())
            overlap = len(qw & aw) / max(len(qw), 1)
            if overlap >= 0.6:
                atom.usage_count += 1
                return atom.to_text()
        return ''

    def _is_rate_limited(self, query: str) -> bool:
        last = self._call_log.get(query.lower(), 0)
        return (time.time() - last) < (self.CACHE_HOURS * 3600)

    def _ddg_search(self, query: str) -> str:
        try:
            enc = urllib.parse.quote(query)
            url = f'https://api.duckduckgo.com/?q={enc}&format=json&no_html=1'
            req = urllib.request.Request(
                url, headers={'User-Agent': 'KA-Mind/2.0 NeuraBrain'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            text = data.get('AbstractText', '')
            if not text:
                topics = data.get('RelatedTopics', [])
                texts  = [t.get('Text','') for t in topics[:3]
                          if isinstance(t,dict)]
                text = ' '.join(texts)
            return text.strip()
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            return ''

    def _save_to_memory(self, query: str, text: str):
        atom = KnowledgeAtom(
            atom_type  = AtomType.FACT,
            content    = {'text': text[:1000], 'source': 'web',
                          'query': query},
            confidence = 0.75,
            source     = 'web_search',
            category   = 'web'
        )
        self.memory.add_atom(atom)

    def read_url(self, url: str) -> str:
        cached = self._check_cache(url)
        if cached: return f'[Cached] {cached}'
        try:
            import re
            req = urllib.request.Request(
                url, headers={'User-Agent':'Mozilla/5.0 KA-Mind/2.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                html = r.read().decode('utf-8', errors='ignore')
            html = re.sub(r'<script[^>]*>.*?</script>','',html,flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>','',html,flags=re.DOTALL)
            text = re.sub(r'<[^>]+>',' ',html)
            text = re.sub(r'\s+',' ',text).strip()[:5000]
            self._save_to_memory(url, text[:1000])
            self._call_log[url.lower()] = time.time()
            return text
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            return f'URL read failed: {e}'
