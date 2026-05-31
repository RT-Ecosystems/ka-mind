# KA-Mind Math Agent — Precise calculations
import math, re
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class MathAgent:
    def __init__(self, memory_graph):
        self.memory = memory_graph

    def solve(self, query: str) -> str:
        # Extract math expression from natural language
        expr = self._extract_expression(query)
        if expr:
            result = self._evaluate(expr)
            if result is not None:
                answer = f'{expr} = {result}'
                self.memory.add_atom(KnowledgeAtom(AtomType.FACT,
                    {'text': answer, 'type': 'math_result'}, 0.99))
                return answer

        # Try word problem solving
        return self._word_problem(query)

    def _extract_expression(self, text: str) -> str:
        patterns = [
            r'[\d\s\+\-\*/\(\)\.\^%]+',
        ]
        text_clean = text.replace('x','*').replace('X','*')
        text_clean = text_clean.replace('^','**')
        for pat in patterns:
            m = re.search(pat, text_clean)
            if m:
                expr = m.group().strip()
                if any(c.isdigit() for c in expr) and len(expr)>1:
                    return expr
        return ''

    def _evaluate(self, expr: str):
        safe = {k:getattr(math,k) for k in dir(math) if not k.startswith('_')}
        safe['abs'] = abs
        try:
            result = eval(expr.replace('^','**'),{'__builtins__':{}},safe)
            if isinstance(result, float):
                return round(result, 6)
            return result
        except: return None

    def _word_problem(self, query: str) -> str:
        q = query.lower()
        # Percentage
        m = re.search(r'(\d+)%\s+of\s+(\d+)', q)
        if m:
            a,b = int(m.group(1)), int(m.group(2))
            return f'{a}% of {b} = {a*b/100}'
        # Simple word numbers
        words = {'one':1,'two':2,'three':3,'four':4,'five':5,
                 'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
        nums = [words[w] for w in q.split() if w in words]
        if len(nums) >= 2:
            if 'plus' in q or 'add' in q: return f'Result = {sum(nums)}'
            if 'times' in q or 'multiply' in q:
                from functools import reduce
                return f'Result = {reduce(lambda a,b:a*b, nums)}'
        return 'Please express the math problem more clearly.'
