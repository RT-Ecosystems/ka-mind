# KA-Mind Code Agent
class CodeAgent:
    TEMPLATES = {
        'sort':'sorted_list = sorted(my_list)',
        'reverse':'reversed_list = my_list[::-1]',
        'sum':'total = sum(my_list)',
        'read':"with open(filename) as f:\n    content = f.read()",
        'write':"with open(filename,'w') as f:\n    f.write(content)",
    }
    def solve_task(self, task: str) -> str:
        tl = task.lower()
        for kw, code in self.TEMPLATES.items():
            if kw in tl: return f'```python\n{code}\n```'
        return f'Task: {task}\nTrain on coding data for better solutions.'
    def execute_safe(self, code: str) -> str:
        bad = ['import os','import sys','__import__','exec(','eval(','open(']
        if any(b in code for b in bad): return 'Blocked: unsafe code.'
        try:
            ns = {}
            exec(code,{'__builtins__':{}},ns)
            return f'Result: {ns}'
        except Exception as e: return f'Error: {e}'
