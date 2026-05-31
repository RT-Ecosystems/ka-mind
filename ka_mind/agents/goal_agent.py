# KA-Mind Goal Agent — Plan and Execute goals
# BUG FIXED: feedback_notes IndexError on first step
from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
import time


class GoalAgent:
    def __init__(self, memory_graph, web_agent=None, neocortex=None):
        self.memory    = memory_graph
        self.web_agent = web_agent
        self.neocortex = neocortex

    def create_plan(self, goal: str) -> list:
        plan = [
            ('search_memory',  f'Search memory graph for: {goal}'),
            ('web_search',     f'If not found, search internet for: {goal}'),
            ('reason',         f'Apply Neocortex reasoning on: {goal}'),
            ('save_feedback',  f'Save learning about: {goal}'),
        ]
        print(f'Goal: {goal} | Plan: {len(plan)} steps')
        return plan

    def execute_plan(self, goal: str) -> dict:
        plan     = self.create_plan(goal)
        feedback = {}
        goal_key = goal.split()[0] if goal.split() else goal

        for step_type, step_desc in plan:
            print(f'  Executing: {step_desc[:60]}')

            if step_type == 'search_memory':
                results = self.memory.search(goal_key)
                if results:
                    feedback['memory'] = f'Found {len(results)} atoms'
                else:
                    feedback['memory'] = 'Not found in memory'

            elif step_type == 'web_search':
                # BUG FIXED: check feedback safely
                mem_result = feedback.get('memory', '')
                if 'Not found' in mem_result and self.web_agent:
                    self.web_agent.search_and_learn(goal)
                    feedback['web'] = 'Learned from internet'
                else:
                    feedback['web'] = 'Skipped (memory had data)'

            elif step_type == 'reason':
                if self.neocortex:
                    thoughts = self.neocortex.think_and_reason()
                    feedback['reasoning'] = f'{len(thoughts)} insights generated'

            elif step_type == 'save_feedback':
                summary = ' | '.join(f'{k}:{v}' for k,v in feedback.items())
                atom = KnowledgeAtom(AtomType.FACT,
                    {'text': f'Goal completed: {goal}. Results: {summary}'},
                    category='system_feedback')
                self.memory.add_atom(atom)
                feedback['saved'] = 'Saved to memory'

            time.sleep(0.1)

        print(f'Goal complete: {goal}')
        return feedback
