# KA-Mind Code Agent — Code generation and execution
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType


class CodeAgent:
    TEMPLATES = {
        'sort':    'sorted_list = sorted(my_list)',
        'reverse': 'reversed_list = my_list[::-1]',
        'sum':     'total = sum(my_list)',
        'read':    'with open(filename) as f:\n    content = f.read()',
        'write':   'with open(filename, w) as f:\n    f.write(content)',
    }

    def solve_task(self, task: str) -> str:
        task_lower = task.lower()
        for kw, code in self.TEMPLATES.items():
            if kw in task_lower:
                return f'Code solution:\n```python\n{code}\n```'
        return (f'Task: {task}\n'
                f'Hint: Train on coding data for domain-specific solutions.')

    def execute_safe(self, code: str) -> str:
        forbidden = ['import os','import sys','__import__',
                     'exec(','eval(','open(','subprocess']
        if any(f in code for f in forbidden):
            return 'Execution blocked: unsafe code detected.'
        try:
            local_ns = {}
            exec(code, {'__builtins__': {}}, local_ns)
            return f'Result: {local_ns}'
        except Exception as e:
            return f'Execution error: {e}'
