# KA-Mind Master Teacher v2.2
# FIXED: SyntaxWarning for invalid escape sequence
import re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
from ka_mind.core.composer import Composer


class MasterTeacher:
    # Math pattern (raw string - FIXED \d warning)
    MATH_PAT = re.compile(r'\d+[\s]*[+\-*/^]')

    def __init__(self, memory_graph, web_agent=None, code_agent=None,
                 vision_agent=None, vector_graph=None, math_agent=None,
                 file_agent=None, memory_agent=None, translator=None,
                 time_agent=None, api_agent=None):
        self.memory      = memory_graph
        self.web         = web_agent
        self.code        = code_agent
        self.vision      = vision_agent
        self.vector      = vector_graph
        self.math        = math_agent
        self.file        = file_agent
        self.mem_agent   = memory_agent
        self.translator  = translator
        self.time        = time_agent
        self.api_agent   = api_agent   # NEW v2.2
        self.composer    = Composer(memory_graph)

    def process_request(self, query: str,
                        user_id: str = 'system') -> str:
        intent = self._intent(query)

        if intent == 'api_connect':
            if self.api_agent:
                return self.api_agent.handle(query)
            return 'API Agent not initialized.'

        if intent == 'time':
            return self.time.answer(query) if self.time else 'Time Agent offline.'

        if intent == 'math':
            return self.math.solve(query) if self.math else 'Math Agent offline.'

        if intent == 'translate':
            if self.translator:
                to   = 'hi' if any(w in query.lower()
                                   for w in ['hindi','हिंदी']) else 'en'
                text = re.sub(r'translate|to hindi|to english|अनुवाद',
                              '', query, flags=re.IGNORECASE).strip()
                return self.translator.translate(text, to)
            return 'Translator offline.'

        if intent == 'remember':
            if self.mem_agent:
                fact = re.sub(r'remember|याद रखो|note that',
                              '', query, flags=re.IGNORECASE).strip()
                return self.mem_agent.remember(fact, user_id)
            return 'Memory Agent offline.'

        if intent == 'recall':
            return (self.mem_agent.recall(query, user_id)
                    if self.mem_agent else 'Memory Agent offline.')

        if intent == 'draw_image':
            if self.vision:
                prompt = re.sub(r'बनाओ|इमेज|draw|image|picture|create',
                                '', query, flags=re.IGNORECASE).strip()
                return self.vision.generate_image(prompt)
            return 'Vision Agent offline.'

        if intent == 'build_code':
            return self.code.solve_task(query) if self.code else 'Code Agent offline.'

        if intent == 'read_file':
            if self.file:
                m = re.search(r'[\w./\\]+\.[a-z]{2,4}', query)
                if m: return self.file.read_and_learn(m.group())
            return 'File Agent offline.'

        if intent == 'web_search':
            if self.web:
                topic = re.sub(r'सर्च|search|इंटरनेट|internet|latest|look up',
                               '', query, flags=re.IGNORECASE).strip()
                return self.web.search_and_learn(topic)
            return 'Web Agent offline.'

        return self._reason_human(query, user_id)

    def _reason_human(self, query: str, user_id: str) -> str:
        graph_results = self.memory.search_scored(query, user_id, top_k=15)
        vector_atoms  = []
        if self.vector and len(self.vector.graph) > 0:
            try:
                va, score = self.vector.search_by_meaning(query)
                if va and score > 0.35: vector_atoms.append(va)
            except: pass
        all_atoms = [a for a, _ in graph_results] + vector_atoms
        if not all_atoms and self.web:
            wr = self.web.search_and_learn(query)
            if '[Web]' in wr:
                new = self.memory.search_scored(query, user_id, top_k=10)
                all_atoms = [a for a, _ in new]
        if not all_atoms:
            return ('I do not have enough knowledge on this topic. '
                    'Train me or ask me to search the web.')
        answer = self.composer.compose_answer(query, all_atoms)
        chain  = self.composer.chain_reason(query, steps=2)
        if len(chain) > 1:
            answer += f' This suggests that {chain[-1].strip()}.'
        return answer

    def _intent(self, text: str) -> str:
        t = text.lower()
        # API connect
        if any(w in t for w in ['connect api','add api','api key','api token',
                                 'connect github','connect slack','api जोड़ो']):
            return 'api_connect'
        # Time
        if any(w in t for w in ['time','समय','date','तारीख','today','आज','कल']):
            return 'time'
        # Math — FIXED: use compiled pattern, no raw string warning
        if (any(w in t for w in ['calculate','%','plus','minus','times'])
                or self.MATH_PAT.search(t)):
            return 'math'
        if any(w in t for w in ['translate','अनुवाद','to hindi','to english']):
            return 'translate'
        if any(w in t for w in ['remember','याद रखो','note that']): return 'remember'
        if any(w in t for w in ['recall','याद करो','what did']):    return 'recall'
        if any(w in t for w in ['इमेज','draw','image','generate image']):
            return 'draw_image'
        if any(w in t for w in ['code','कोड','script','program']): return 'build_code'
        if any(w in t for w in ['.pdf','.docx','.csv','read file']): return 'read_file'
        if any(w in t for w in ['search','सर्च','latest','इंटरनेट']):
            return 'web_search'
        return 'general_reasoning'

    def _no_agent(self, name): return f'{name} Agent offline.'
