# KA-Mind Master Teacher v2.1
# All agents integrated + human language output
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
from ka_mind.core.composer import Composer


class MasterTeacher:
    def __init__(self, memory_graph, web_agent=None, code_agent=None,
                 vision_agent=None, vector_graph=None, math_agent=None,
                 file_agent=None, memory_agent=None, translator=None,
                 time_agent=None):
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
        self.composer    = Composer(memory_graph)

    def process_request(self, query: str,
                        user_id: str = 'system') -> str:
        intent = self._intent(query)

        if intent == 'time':
            return self.time.answer(query) if self.time else self._no_agent('Time')

        if intent == 'math':
            return self.math.solve(query) if self.math else self._no_agent('Math')

        if intent == 'translate':
            if self.translator:
                to   = 'hi' if any(w in query.lower() for w in ['hindi','हिंदी']) else 'en'
                text = re.sub(r'translate|to hindi|to english|अनुवाद','',
                              query,flags=re.IGNORECASE).strip()
                return self.translator.translate(text, to)
            return self._no_agent('Translator')

        if intent == 'remember':
            if self.mem_agent:
                fact = re.sub(r'remember|याद रखो|note that','',
                              query,flags=re.IGNORECASE).strip()
                return self.mem_agent.remember(fact, user_id)
            return self._no_agent('Memory')

        if intent == 'recall':
            return self.mem_agent.recall(query,user_id) if self.mem_agent else self._no_agent('Memory')

        if intent == 'draw_image':
            if self.vision:
                prompt = re.sub(r'बनाओ|इमेज|draw|image|picture|create',
                                '',query,flags=re.IGNORECASE).strip()
                return self.vision.generate_image(prompt)
            return self._no_agent('Vision')

        if intent == 'build_code':
            return self.code.solve_task(query) if self.code else self._no_agent('Code')

        if intent == 'read_file':
            if self.file:
                import re as re2
                path = re2.search(r'[\w./\\]+\.[a-z]{2,4}', query)
                if path: return self.file.read_and_learn(path.group())
            return self._no_agent('File')

        if intent == 'web_search':
            if self.web:
                topic = re.sub(r'सर्च|search|इंटरनेट|internet|latest|look up',
                               '',query,flags=re.IGNORECASE).strip()
                return self.web.search_and_learn(topic)
            return self._no_agent('Web')

        # Default: reason from memory with human language
        return self._reason_human(query, user_id)

    def _reason_human(self, query: str, user_id: str) -> str:
        # 1. Graph memory search
        graph_results = self.memory.search_scored(query, user_id, top_k=15)

        # 2. Vector semantic search
        vector_atoms = []
        if self.vector and len(self.vector.graph) > 0:
            try:
                va, score = self.vector.search_by_meaning(query)
                if va and score > 0.35: vector_atoms.append(va)
            except: pass

        all_atoms = [a for a,_ in graph_results] + vector_atoms

        if not all_atoms:
            # 3. Fallback: web search automatically
            if self.web:
                web_result = self.web.search_and_learn(query)
                if '[Web]' in web_result:
                    new_results = self.memory.search_scored(query,user_id,top_k=10)
                    all_atoms   = [a for a,_ in new_results]

        if not all_atoms:
            return ('I do not have enough knowledge on this topic. '
                    'Train me with domain data or ask me to search the web.')

        # 4. Human-like answer via Composer + HumanLanguageEngine
        answer = self.composer.compose_answer(query, all_atoms)

        # 5. Chain reasoning suffix
        chain = self.composer.chain_reason(query, steps=2)
        if len(chain) > 1:
            reasoning = chain[-1].strip()
            answer += f' This suggests that {reasoning}.'

        return answer

    def _intent(self, text: str) -> str:
        import re
        t = text.lower()
        if any(w in t for w in ['time','समय','date','तारीख','today','आज','कल','tomorrow']):
            return 'time'
        if any(w in t for w in ['calculate','=','%','plus','minus','times','\d+[+\-*/]']):
            return 'math'
        if re.search(r'\d+[\s]*[+\-*/^]', t): return 'math'
        if any(w in t for w in ['translate','अनुवाद','to hindi','to english']): return 'translate'
        if any(w in t for w in ['remember','याद रखो','note that']): return 'remember'
        if any(w in t for w in ['recall','याद करो','what did']): return 'recall'
        if any(w in t for w in ['इमेज','फोटो','draw','image','generate image']): return 'draw_image'
        if any(w in t for w in ['कोड','code','script','program']): return 'build_code'
        if any(w in t for w in ['read file','file पढ़ो','.pdf','.docx','.csv']): return 'read_file'
        if any(w in t for w in ['search','सर्च','latest','इंटरनेट']): return 'web_search'
        return 'general_reasoning'

    def _no_agent(self, name: str) -> str:
        return f'{name} Agent is not connected. Initialize KaModel to use all agents.'
