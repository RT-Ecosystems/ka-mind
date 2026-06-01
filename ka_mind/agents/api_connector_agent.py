# KA-Mind API Connector Agent v2.3
# FIXED: sk- collision (OpenAI vs DeepSeek vs OpenRouter)
# Solution: endpoint verification when prefix is ambiguous
import urllib.request, urllib.parse, json, re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class APIConnectorAgent:

    KNOWN_APIS = {
        'github': {
            'test_url':      'https://api.github.com/user',
            'auth_type':     'bearer',
            'prefix':        ['ghp_', 'github_pat_', 'gho_', 'ghu_'],
            'ambiguous':     False,
            'capabilities':  ['repos','issues','code search','commits','gists'],
            'description':   'GitHub — code repos and developer tools'
        },
        'openai': {
            'test_url':      'https://api.openai.com/v1/models',
            'auth_type':     'bearer',
            'prefix':        ['sk-'],
            'ambiguous':     True,
            'capabilities':  ['chat','image generation','embeddings','audio'],
            'description':   'OpenAI — GPT, DALL-E, Whisper'
        },
        'anthropic': {
            'test_url':      'https://api.anthropic.com/v1/models',
            'auth_type':     'x-api-key',
            'prefix':        ['sk-ant-'],
            'ambiguous':     False,
            'capabilities':  ['chat','analysis','coding'],
            'description':   'Anthropic — Claude models'
        },
        'deepseek': {
            'test_url':      'https://api.deepseek.com/v1/models',
            'auth_type':     'bearer',
            'prefix':        ['sk-'],
            'ambiguous':     True,
            'capabilities':  ['chat','code generation','reasoning'],
            'description':   'DeepSeek — powerful reasoning model'
        },
        'openrouter': {
            'test_url':      'https://openrouter.ai/api/v1/models',
            'auth_type':     'bearer',
            'prefix':        ['sk-or-'],
            'ambiguous':     False,
            'capabilities':  ['multi-model routing','100+ models'],
            'description':   'OpenRouter — access any AI model'
        },
        'huggingface': {
            'test_url':      'https://huggingface.co/api/whoami',
            'auth_type':     'bearer',
            'prefix':        ['hf_'],
            'ambiguous':     False,
            'capabilities':  ['models','datasets','inference'],
            'description':   'HuggingFace — AI models hub'
        },
        'slack': {
            'test_url':      'https://slack.com/api/auth.test',
            'auth_type':     'bearer',
            'prefix':        ['xoxb-','xoxp-','xoxa-'],
            'ambiguous':     False,
            'capabilities':  ['messaging','channels','search'],
            'description':   'Slack — team messaging'
        },
        'notion': {
            'test_url':      'https://api.notion.com/v1/users/me',
            'auth_type':     'bearer_notion',
            'prefix':        ['secret_','ntn_'],
            'ambiguous':     False,
            'capabilities':  ['pages','databases','blocks'],
            'description':   'Notion — notes and databases'
        },
        'weather': {
            'test_url':      'https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}',
            'auth_type':     'url_param',
            'prefix':        [],
            'ambiguous':     False,
            'capabilities':  ['current weather','forecast'],
            'description':   'OpenWeatherMap — weather data'
        },
        'telegram': {
            'test_url':      'https://api.telegram.org/bot{key}/getMe',
            'auth_type':     'url_param',
            'prefix':        [],
            'ambiguous':     False,
            'capabilities':  ['bot messaging','notifications'],
            'description':   'Telegram Bot API'
        },
    }

    # APIs that share the same prefix → need endpoint verification
    AMBIGUOUS_GROUPS = {
        'sk-': ['openai', 'deepseek'],   # sk-or- handled separately (more specific)
    }

    def __init__(self, memory_graph):
        self.memory     = memory_graph
        self.registered = {}

    def handle(self, query: str) -> str:
        key_match = re.search(
            r'(?:key|token|api)[:\s]+([A-Za-z0-9_\-\.]{10,})',
            query, re.IGNORECASE)
        if key_match:
            api_key = key_match.group(1).strip()
        else:
            words = query.split()
            candidates = [w for w in words
                          if len(w) > 12
                          and not w.lower().startswith(
                              ('connect','add','api','use'))]
            if not candidates:
                return self._help_message()
            api_key = candidates[0]
        name_hint = None
        for api_name in self.KNOWN_APIS:
            if api_name in query.lower():
                name_hint = api_name
                break
        return self.add_api(api_key, name_hint)

    def add_api(self, api_key: str, api_name: str = None) -> str:
        if not api_name:
            api_name = self._detect(api_key)
        if not api_name:
            return ('Could not detect API type. Supported: '
                    + ', '.join(self.KNOWN_APIS.keys()))
        is_valid = self._verify(api_key, api_name)
        if not is_valid:
            return f'API key verification failed for {api_name}.'
        info = self.KNOWN_APIS[api_name]
        self.registered[api_name] = {'key': api_key,
                                      'capabilities': info['capabilities']}
        self.memory.add_atom(KnowledgeAtom(AtomType.FACT,
            {'text': f'{api_name} API connected',
             'api': api_name, 'safe': True}, 0.99, 'api_agent'))
        caps = ', '.join(info['capabilities'])
        return (f'Connected: {api_name.upper()}\n'
                f'Info: {info["description"]}\n'
                f'Can do: {caps}')

    def _detect(self, key: str) -> str:
        # Step 1: More specific prefixes first (sk-or- before sk-)
        specific_first = sorted(
            self.KNOWN_APIS.items(),
            key=lambda x: max((len(p) for p in x[1]['prefix']), default=0),
            reverse=True
        )
        # Step 2: Find all matching APIs
        matches = []
        for name, config in specific_first:
            for prefix in config['prefix']:
                if key.startswith(prefix):
                    matches.append(name)
                    break
        if not matches:
            return self._try_all(key)
        if len(matches) == 1:
            return matches[0]
        # Step 3: Ambiguous (multiple matches) → verify each
        print(f'  Ambiguous prefix. Testing endpoints: {matches}...')
        for name in matches:
            if self._verify(key, name):
                print(f'  Detected: {name}')
                return name
        return matches[0]

    def _verify(self, key: str, api_name: str) -> bool:
        config    = self.KNOWN_APIS.get(api_name, {})
        url       = config.get('test_url','').replace('{key}', key)
        auth_type = config.get('auth_type','bearer')
        if not url: return False
        try:
            headers = {'User-Agent': 'KA-Mind/2.3'}
            if auth_type == 'bearer':
                headers['Authorization'] = f'Bearer {key}'
            elif auth_type == 'x-api-key':
                headers['x-api-key'] = key
                headers['anthropic-version'] = '2023-06-01'
            elif auth_type == 'bearer_notion':
                headers['Authorization'] = f'Bearer {key}'
                headers['Notion-Version'] = '2022-06-28'
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as r:
                return r.status == 200
        except urllib.error.HTTPError as e:
            return e.code not in [401, 403]
        except Exception:
            return False

    def _try_all(self, key: str) -> str:
        order = ['github','openai','anthropic','deepseek','huggingface',
                 'slack','notion','openrouter']
        for name in order:
            if self._verify(key, name):
                return name
        return None

    def use_github(self, command: str) -> str:
        if 'github' not in self.registered:
            return 'GitHub not connected. Say: connect github api <token>'
        key = self.registered['github']['key']
        cmd = command.lower()
        if 'my repos' in cmd or 'list repos' in cmd:
            return self._gh('/user/repos?per_page=10', key)
        if 'profile' in cmd or 'user info' in cmd:
            return self._gh('/user', key)
        m = re.search(r'([\w-]+)/([\w-]+)', command)
        if 'issues' in cmd and m:
            return self._gh(f'/repos/{m.group(1)}/{m.group(2)}/issues', key)
        if 'search' in cmd:
            q = urllib.parse.quote(re.sub(r'search|github','',cmd).strip())
            return self._gh(f'/search/repositories?q={q}&per_page=5', key)
        return 'GitHub: say repos / issues / profile / search'

    def _gh(self, endpoint: str, key: str) -> str:
        try:
            req = urllib.request.Request(
                f'https://api.github.com{endpoint}',
                headers={'Authorization': f'Bearer {key}',
                         'Accept': 'application/vnd.github.v3+json',
                         'User-Agent': 'KA-Mind/2.3'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            if isinstance(data, list):
                lines = []
                for item in data[:5]:
                    n = item.get('name') or item.get('title','')
                    u = item.get('html_url','')
                    lines.append(f'  - {n}: {u}')
                return '\n'.join(lines) or 'Empty.'
            login = data.get('login', data.get('full_name',''))
            name  = data.get('name','')
            bio   = data.get('bio','') or ''
            return f'GitHub: {login} ({name}). {bio}'
        except Exception as e:
            return f'GitHub error: {e}'

    def list_connected(self) -> str:
        if not self.registered: return 'No APIs connected.'
        lines = ['Connected APIs:']
        for name, info in self.registered.items():
            lines.append(f'  {name.upper()}: {info["capabilities"][:2]}')
        return '\n'.join(lines)

    def _help_message(self) -> str:
        return ('API Connector:\n'
                '  connect github api ghp_token\n'
                '  connect openai api sk-token\n'
                '  connect deepseek api sk-token\n'
                '  connect slack api xoxb-token\n'
                'Supported: ' + ', '.join(self.KNOWN_APIS.keys()))
