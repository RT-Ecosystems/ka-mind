# KA-Mind API Connector Agent
# Auto-detects API type, validates, creates named agent
# User brings any API key -> agent figures out what it is
import urllib.request, urllib.parse, json, re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class APIConnectorAgent:

    # Known APIs: how to detect and what they can do
    KNOWN_APIS = {
        'github': {
            'test_url':   'https://api.github.com/user',
            'auth_type':  'bearer',
            'detect_prefix': ['ghp_', 'github_pat_'],
            'capabilities': ['repos','issues','code search','commits','gists'],
            'description': 'GitHub — code repos, issues, developer tools'
        },
        'openai': {
            'test_url':   'https://api.openai.com/v1/models',
            'auth_type':  'bearer',
            'detect_prefix': ['sk-'],
            'capabilities': ['chat','image generation','embeddings','audio'],
            'description': 'OpenAI — GPT models, DALL-E, Whisper'
        },
        'slack': {
            'test_url':   'https://slack.com/api/auth.test',
            'auth_type':  'bearer',
            'detect_prefix': ['xoxb-', 'xoxp-', 'xoxa-'],
            'capabilities': ['send message','read channels','search messages'],
            'description': 'Slack — team messaging'
        },
        'telegram': {
            'test_url':   'https://api.telegram.org/bot{key}/getMe',
            'auth_type':  'url_param',
            'detect_prefix': [],
            'capabilities': ['send message','bot control','notifications'],
            'description': 'Telegram Bot API'
        },
        'notion': {
            'test_url':   'https://api.notion.com/v1/users/me',
            'auth_type':  'bearer',
            'detect_prefix': ['secret_'],
            'capabilities': ['pages','databases','blocks'],
            'description': 'Notion — notes and databases'
        },
        'weather': {
            'test_url':   'https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}',
            'auth_type':  'url_param',
            'detect_prefix': [],
            'capabilities': ['current weather','forecast','alerts'],
            'description': 'OpenWeatherMap — weather data'
        },
        'huggingface': {
            'test_url':   'https://huggingface.co/api/whoami',
            'auth_type':  'bearer',
            'detect_prefix': ['hf_'],
            'capabilities': ['models','datasets','inference'],
            'description': 'HuggingFace — AI models hub'
        },
    }

    def __init__(self, memory_graph):
        self.memory     = memory_graph
        self.registered = {}  # name -> {key, capabilities}

    def handle(self, query: str) -> str:
        q = query.lower()
        # Extract API key from query
        key_match = re.search(
            r'(?:key|token|api)[:\s]+([A-Za-z0-9_\-\.]{10,})', query,
            re.IGNORECASE)
        if not key_match:
            # Maybe the key IS the query (user pasted it)
            words = query.split()
            candidates = [w for w in words if len(w) > 15
                          and not w.lower().startswith(('connect','add','api'))]
            if candidates:
                api_key = candidates[0]
            else:
                return self._help_message()
        else:
            api_key = key_match.group(1).strip()

        # Check if name hint given
        name_hint = None
        for api_name in self.KNOWN_APIS:
            if api_name in q:
                name_hint = api_name
                break

        return self.add_api(api_key, name_hint)

    def add_api(self, api_key: str, api_name: str = None) -> str:
        # Step 1: Auto-detect if no name given
        if not api_name:
            api_name = self._detect_by_prefix(api_key)

        # Step 2: Try to verify
        if api_name and api_name in self.KNOWN_APIS:
            is_valid = self._verify(api_key, api_name)
        else:
            # Try all APIs to find which one this key works for
            api_name, is_valid = self._try_all(api_key)

        if not is_valid or not api_name:
            return ('API key could not be verified. '
                    'Supported: ' + ', '.join(self.KNOWN_APIS.keys()))

        # Step 3: Register
        info = self.KNOWN_APIS[api_name]
        self.registered[api_name] = {
            'key': api_key,
            'capabilities': info['capabilities'],
            'description': info['description']
        }
        # Save to memory
        self.memory.add_atom(KnowledgeAtom(AtomType.FACT,
            {'text': f'{api_name} API connected',
             'api_name': api_name,
             'capabilities': ', '.join(info['capabilities']),
             'safe': True}, 0.99, 'api_agent'))

        caps = ', '.join(info['capabilities'])
        return (
            f'✅ {api_name.upper()} API connected!\n'
            f'Description: {info["description"]}\n'
            f'Capabilities: {caps}\n'
            f'Usage: ask me to use {api_name} for any task.'
        )

    def _detect_by_prefix(self, key: str) -> str:
        for name, config in self.KNOWN_APIS.items():
            for prefix in config.get('detect_prefix', []):
                if key.startswith(prefix):
                    return name
        return None

    def _verify(self, key: str, api_name: str) -> bool:
        config  = self.KNOWN_APIS[api_name]
        url     = config['test_url'].replace('{key}', key)
        auth_type = config['auth_type']
        try:
            if auth_type == 'bearer':
                req = urllib.request.Request(
                    url, headers={'Authorization': f'Bearer {key}',
                                  'User-Agent': 'KA-Mind/2.2'})
            else:
                req = urllib.request.Request(
                    url, headers={'User-Agent': 'KA-Mind/2.2'})
            with urllib.request.urlopen(req, timeout=8) as r:
                return r.status == 200
        except urllib.error.HTTPError as e:
            return e.code not in [401, 403]  # 404 still means key works
        except Exception:
            return False

    def _try_all(self, key: str):
        # Prefix detection first (fast)
        detected = self._detect_by_prefix(key)
        if detected:
            return detected, self._verify(key, detected)
        # Try each API (slower)
        for name in ['github', 'openai', 'slack', 'notion', 'huggingface']:
            if self._verify(key, name):
                return name, True
        return None, False

    def use_github(self, command: str) -> str:
        if 'github' not in self.registered:
            return 'GitHub API not connected. Say: connect github api <your-token>'
        key = self.registered['github']['key']
        cmd = command.lower()

        if 'my repos' in cmd or 'list repos' in cmd:
            return self._github_api('/user/repos?per_page=10', key)
        if 'issues' in cmd:
            m = re.search(r'([\w-]+)/([\w-]+)', command)
            if m:
                return self._github_api(f'/repos/{m.group(1)}/{m.group(2)}/issues', key)
        if 'profile' in cmd or 'user' in cmd:
            return self._github_api('/user', key)
        if 'search' in cmd:
            q = urllib.parse.quote(re.sub(r'search|github','',cmd).strip())
            return self._github_api(f'/search/repositories?q={q}&per_page=5', key)
        return 'GitHub: say repos/issues/profile/search'

    def _github_api(self, endpoint: str, key: str) -> str:
        try:
            url = f'https://api.github.com{endpoint}'
            req = urllib.request.Request(url, headers={
                'Authorization': f'Bearer {key}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'KA-Mind/2.2'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            if isinstance(data, list):
                results = []
                for item in data[:5]:
                    name = item.get('name') or item.get('title', '')
                    url  = item.get('html_url', '')
                    results.append(f'  - {name}: {url}')
                return '\n'.join(results) if results else 'No results.'
            else:
                login = data.get('login', data.get('full_name', ''))
                name  = data.get('name', '')
                return f'GitHub User: {login} ({name})'
        except Exception as e:
            return f'GitHub API error: {e}'

    def use_weather(self, city: str) -> str:
        if 'weather' not in self.registered:
            return 'Weather API not connected.'
        key = self.registered['weather']['key']
        try:
            enc = urllib.parse.quote(city)
            url = f'https://api.openweathermap.org/data/2.5/weather?q={enc}&appid={key}&units=metric'
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            hum  = data['main']['humidity']
            return f'{city}: {temp}°C, {desc}, Humidity: {hum}%'
        except Exception as e:
            return f'Weather error: {e}'

    def list_connected(self) -> str:
        if not self.registered:
            return 'No APIs connected yet.'
        lines = ['Connected APIs:']
        for name, info in self.registered.items():
            caps = ', '.join(info['capabilities'][:3])
            lines.append(f'  {name.upper()}: {caps}')
        return '\n'.join(lines)

    def _help_message(self) -> str:
        supported = ', '.join(self.KNOWN_APIS.keys())
        return (
            f'API Connector Usage:\n'
            f'  connect github api ghp_yourtoken\n'
            f'  connect slack api xoxb-yourtoken\n'
            f'  api key sk-yourkey\n'
            f'Supported: {supported}'
        )
