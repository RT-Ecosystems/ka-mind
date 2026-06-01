# KA-Mind API Connector v2.3.1
# HOTFIX: longest prefix wins → sk-ant- = anthropic (no network needed)
# HOTFIX: only call network when prefix is truly ambiguous
import urllib.request, urllib.parse, json, re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class APIConnectorAgent:

    KNOWN_APIS = {
        'anthropic': {
            'test_url':  'https://api.anthropic.com/v1/models',
            'auth_type': 'x-api-key',
            'prefix':    ['sk-ant-'],
            'capabilities': ['chat','analysis','coding'],
            'description': 'Anthropic — Claude models'
        },
        'openrouter': {
            'test_url':  'https://openrouter.ai/api/v1/models',
            'auth_type': 'bearer',
            'prefix':    ['sk-or-'],
            'capabilities': ['100+ AI models','routing'],
            'description': 'OpenRouter — any AI model'
        },
        'openai': {
            'test_url':  'https://api.openai.com/v1/models',
            'auth_type': 'bearer',
            'prefix':    ['sk-proj-', 'sk-svcacct-'],
            'ambiguous_prefix': 'sk-',
            'capabilities': ['chat','image','audio'],
            'description': 'OpenAI — GPT, DALL-E'
        },
        'deepseek': {
            'test_url':  'https://api.deepseek.com/v1/models',
            'auth_type': 'bearer',
            'prefix':    [],
            'ambiguous_prefix': 'sk-',
            'capabilities': ['chat','code','reasoning'],
            'description': 'DeepSeek — powerful reasoning'
        },
        'github': {
            'test_url':  'https://api.github.com/user',
            'auth_type': 'bearer',
            'prefix':    ['ghp_','github_pat_','gho_','ghu_'],
            'capabilities': ['repos','issues','code search'],
            'description': 'GitHub — developer tools'
        },
        'huggingface': {
            'test_url':  'https://huggingface.co/api/whoami',
            'auth_type': 'bearer',
            'prefix':    ['hf_'],
            'capabilities': ['models','datasets','inference'],
            'description': 'HuggingFace — AI hub'
        },
        'slack': {
            'test_url':  'https://slack.com/api/auth.test',
            'auth_type': 'bearer',
            'prefix':    ['xoxb-','xoxp-','xoxa-'],
            'capabilities': ['messaging','channels'],
            'description': 'Slack — team messaging'
        },
        'notion': {
            'test_url':  'https://api.notion.com/v1/users/me',
            'auth_type': 'bearer_notion',
            'prefix':    ['secret_','ntn_'],
            'capabilities': ['pages','databases'],
            'description': 'Notion — notes and databases'
        },
        'weather': {
            'test_url':  'https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}',
            'auth_type': 'url_param',
            'prefix':    [],
            'capabilities': ['weather','forecast'],
            'description': 'OpenWeatherMap'
        },
        'telegram': {
            'test_url':  'https://api.telegram.org/bot{key}/getMe',
            'auth_type': 'url_param',
            'prefix':    [],
            'capabilities': ['bot','notifications'],
            'description': 'Telegram Bot'
        },
    }

    def __init__(self, memory_graph):
        self.memory     = memory_graph
        self.registered = {}

    def handle(self, query: str) -> str:
        m = re.search(r'(?:key|token|api)[:\s]+([A-Za-z0-9_\-\.]{10,})',
                      query, re.IGNORECASE)
        if m:
            api_key = m.group(1).strip()
        else:
            words = [w for w in query.split()
                     if len(w) > 12
                     and not w.lower().startswith(
                         ('connect','add','api','use','the'))]
            if not words: return self._help()
            api_key = words[0]
        hint = next((n for n in self.KNOWN_APIS if n in query.lower()), None)
        return self.add_api(api_key, hint)

    def add_api(self, key: str, name: str = None) -> str:
        if not name:
            name = self._detect(key)
        if not name:
            return 'Could not detect API. Supported: ' + ', '.join(self.KNOWN_APIS)
        if not self._verify(key, name):
            return f'Verification failed for {name}.'
        info = self.KNOWN_APIS[name]
        reg_caps = info.get('capabilities', [])
        self.registered[name] = {'key': key, 'caps': reg_caps}
        self.memory.add_atom(KnowledgeAtom(AtomType.FACT,
            {'text': f'{name} API connected', 'api': name, 'safe': True},
            0.99, 'api_agent'))
        return (f'Connected: {name.upper()}\n'
                f'Info: {info["description"]}\n'
                f'Can do: {", ".join(info["capabilities"])}')

    def _detect(self, key: str) -> str:
        # HOTFIX: Sort by prefix length DESC → longest match wins
        # sk-ant- (7) > sk-or- (6) > sk-proj- (8) > sk- (3)
        # So sk-ant-xxx → anthropic immediately, no network needed
        all_prefixes = []
        for name, cfg in self.KNOWN_APIS.items():
            for prefix in cfg.get('prefix', []):
                all_prefixes.append((len(prefix), prefix, name))
        all_prefixes.sort(reverse=True)  # longest first

        for _, prefix, name in all_prefixes:
            if key.startswith(prefix):
                return name  # STOP — longest match wins

        # Check ambiguous prefix (sk- without specific suffix)
        if key.startswith('sk-'):
            return self._verify_ambiguous(key, ['openai', 'deepseek'])

        return self._try_all(key)

    def _verify_ambiguous(self, key: str, candidates: list) -> str:
        print(f'  Ambiguous sk- key. Verifying: {candidates}...')
        for name in candidates:
            if self._verify(key, name):
                print(f'  Detected: {name}')
                return name
        return candidates[0]

    def _verify(self, key: str, name: str) -> bool:
        cfg       = self.KNOWN_APIS.get(name, {})
        url       = cfg.get('test_url','').replace('{key}', key)
        auth_type = cfg.get('auth_type','bearer')
        if not url: return False
        try:
            hdrs = {'User-Agent': 'KA-Mind/2.3.1'}
            if auth_type == 'bearer':
                hdrs['Authorization'] = f'Bearer {key}'
            elif auth_type == 'x-api-key':
                hdrs['x-api-key'] = key
                hdrs['anthropic-version'] = '2023-06-01'
            elif auth_type == 'bearer_notion':
                hdrs['Authorization'] = f'Bearer {key}'
                hdrs['Notion-Version'] = '2022-06-28'
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=6) as r:
                return r.status == 200
        except urllib.error.HTTPError as e:
            return e.code not in [401, 403]
        except Exception:
            return False

    def _try_all(self, key: str) -> str:
        for name in ['github','openai','huggingface','slack','notion']:
            if self._verify(key, name): return name
        return None

    def use_github(self, command: str) -> str:
        if 'github' not in self.registered:
            return 'GitHub not connected.'
        key = self.registered['github']['key']
        cmd = command.lower()
        if 'my repos' in cmd: return self._gh('/user/repos?per_page=10', key)
        if 'profile' in cmd:  return self._gh('/user', key)
        m = re.search(r'([\w-]+)/([\w-]+)', command)
        if 'issues' in cmd and m:
            return self._gh(f'/repos/{m.group(1)}/{m.group(2)}/issues', key)
        if 'search' in cmd:
            q = urllib.parse.quote(re.sub(r'search|github','',cmd).strip())
            return self._gh(f'/search/repositories?q={q}&per_page=5', key)
        return 'GitHub: repos / issues / profile / search'

    def _gh(self, ep: str, key: str) -> str:
        try:
            req = urllib.request.Request(
                f'https://api.github.com{ep}',
                headers={'Authorization': f'Bearer {key}',
                         'Accept': 'application/vnd.github.v3+json',
                         'User-Agent': 'KA-Mind/2.3.1'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            if isinstance(data, list):
                return '\n'.join(
                    f'  - {i.get("name","")}: {i.get("html_url","")}'
                    for i in data[:5]) or 'Empty.'
            return f'GitHub: {data.get("login","")} ({data.get("name","")})'
        except Exception as e: return f'GitHub error: {e}'

    def list_connected(self) -> str:
        if not self.registered: return 'No APIs connected.'
        return '\n'.join(
            f'  {n.upper()}: {", ".join(i["caps"][:2])}'
            for n, i in self.registered.items())

    def _help(self) -> str:
        return ('Usage:\n'
                '  connect github api ghp_xxx\n'
                '  connect openai api sk-xxx\n'
                '  connect anthropic api sk-ant-xxx\n'
                '  connect deepseek api sk-xxx\n'
                'Supported: ' + ', '.join(self.KNOWN_APIS))
