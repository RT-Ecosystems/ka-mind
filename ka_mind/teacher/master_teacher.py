# KA-Mind Master Teacher
# BUG FIXED: general_reasoning now searches GraphMemory
# BUG FIXED: VectorGraph used for semantic search
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
from ka_mind.core.composer import Composer


class MasterTeacher:
    def __init__(self, memory_graph, web_agent=None, code_agent=None,
                 vision_agent=None, vector_graph=None):
        self.memory       = memory_graph
        self.web_agent    = web_agent
        self.code_agent   = code_agent
        self.vision_agent = vision_agent
        self.vector_graph = vector_graph
        self.composer     = Composer(memory_graph)

    def process_request(self, user_query: str,
                        user_id: str = 'system') -> str:
        intent = self._analyze_intent(user_query)

        if intent == 'draw_image':
            if self.vision_agent:
                prompt = user_query
                for w in ['बनाओ','इमेज','एक','draw','image','picture','create']:
                    prompt = prompt.replace(w, '')
                return self.vision_agent.generate_image(prompt.strip())
            return 'Vision Agent offline.'

        if intent == 'build_code':
            if self.code_agent:
                return self.code_agent.solve_task(user_query)
            return 'Code Agent offline.'

        if intent == 'web_search':
            if self.web_agent:
                topic = user_query
                for w in ['सर्च करो','के बारे में बताओ','search','tell me about']:
                    topic = topic.replace(w, '')
                return self.web_agent.search_and_learn(topic.strip())
            return 'Web Agent offline.'

        # BUG3 FIX: general_reasoning now searches memory!
        return self._reason_from_memory(user_query, user_id)

    def _reason_from_memory(self, query: str, user_id: str) -> str:
        # Step 1: Search GraphMemory (keyword match)
        graph_results = self.memory.search_scored(query, user_id, top_k=15)

        # Step 2: Search VectorGraph (semantic / meaning-based)
        # BUG4 FIX: VectorGraph is now actually used!
        vector_results = []
        if self.vector_graph and len(self.vector_graph.graph) > 0:
            try:
                va, score = self.vector_graph.search_by_meaning(query)
                if va and score > 0.4:
                    vector_results.append(va)
            except Exception:
                pass

        if not graph_results and not vector_results:
            return ('I do not have enough knowledge on this topic yet. '
                    'Please train me with relevant data first.')

        atoms = [a for a, _ in graph_results] + vector_results

        # Step 3: Composer builds the answer
        answer = self.composer.compose_answer(query, atoms)

        # Step 4: Chain reasoning for depth
        chain = self.composer.chain_reason(query, steps=3)
        if len(chain) > 1:
            reasoning = ' '.join(chain[1:])
            answer += f' | Reasoning: {reasoning}'

        return answer

    def _analyze_intent(self, text: str) -> str:
        text = text.lower()
        visual = ['इमेज','फोटो','पिक्चर','draw','image','picture','generate image']
        code   = ['कोड','code','script','program','function','calculate','कैलकुलेशन']
        web    = ['सर्च','इंटरनेट','के बारे में बताओ','search','look up','latest']
        if any(w in text for w in visual): return 'draw_image'
        if any(w in text for w in code):   return 'build_code'
        if any(w in text for w in web):    return 'web_search'
        return 'general_reasoning'
