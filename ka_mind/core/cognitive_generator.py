# KA-Mind Cognitive Generator
# BUG FIXED: Actual generation using knowledge atoms (not placeholder)
from ka_mind.core.knowledge_atom import AtomType
from ka_mind.core.composer import Composer


class CognitiveGenerator:
    def __init__(self, memory_graph):
        self.memory   = memory_graph
        self.composer = Composer(memory_graph)

    def check_safety(self, task: str) -> bool:
        dangerous = ['hack','malware','virus','attack','steal','exploit',
                     'नुकसान','हैक','बम','weapon','bomb']
        task_lower = task.lower()
        allowed_security = ['ethical hacking','penetration testing',
                            'bug bounty','security research','ctf','defensive']
        if any(w in task_lower for w in dangerous):
            if any(a in task_lower for a in allowed_security):
                return True  # Security research is ok
            print(f'SAFETY BLOCK: {task[:50]}')
            return False
        return True

    def generate(self, task: str, skill_type: str = 'general') -> str:
        if not self.check_safety(task):
            return 'Access Denied: Request violates safety rules.'

        # Search relevant atoms for the task
        relevant = self.memory.search_scored(task, top_k=10)
        atoms    = [a for a, _ in relevant
                    if a.content.get('skill') == skill_type or skill_type == 'general']
        if not atoms:
            atoms = [a for a, _ in relevant]

        if not atoms:
            return (f'No knowledge found for task: {task}. '
                    f'Train on {skill_type} data first.')

        # Use composer to build answer
        return self.composer.compose_answer(task, atoms)
