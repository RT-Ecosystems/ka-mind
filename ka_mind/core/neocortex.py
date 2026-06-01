# KA-Mind Neocortex v2.3
# Now uses ReasoningEngine — real logic, not 'combined insight'
from .knowledge_atom import AtomType
from .reasoning_engine import ReasoningEngine


class Neocortex:
    def __init__(self, memory_graph):
        self.memory  = memory_graph
        self.engine  = ReasoningEngine(memory_graph)

    def reason_about(self, query: str) -> str:
        return self.engine.reason(query)

    def think_and_reason(self) -> list:
        derived = self.engine.forward_chain(max_steps=3)
        if derived:
            return derived[:10]
        return ['No new conclusions derivable from current knowledge.']

    def detect_contradictions(self) -> list:
        alerts = []
        facts  = list(self.memory.graph.values())
        neg_words = ['not','no','never','false','incorrect',
                     'नहीं','न','गलत','असत्य']

        for i, a1 in enumerate(facts):
            for a2 in facts[i+1:]:
                t1 = a1.to_text().lower()
                t2 = a2.to_text().lower()
                for neg in neg_words:
                    if (t1.replace(f' {neg} ','') == t2 or
                            t2.replace(f' {neg} ','') == t1):
                        a1.confidence = max(0.0, a1.confidence - 0.3)
                        a2.confidence = max(0.0, a2.confidence - 0.3)
                        alerts.append(f'CONTRADICTION: [{t1[:50]}] vs [{t2[:50]}]')
                s1 = a1.content.get('subject','')
                s2 = a2.content.get('subject','')
                p1 = a1.content.get('predicate','')
                p2 = a2.content.get('predicate','')
                o1 = a1.content.get('object','')
                o2 = a2.content.get('object','')
                if (s1 and s1 == s2 and p1 == p2 == 'is'
                        and o1 and o2 and o1 != o2
                        and len(o1) > 2 and len(o2) > 2):
                    alerts.append(f'CONFLICT: {s1} is [{o1}] vs [{o2}]')
        return alerts[:10]

    def run_deep_sleep_cycle(self):
        print('Neocortex: deep sleep started...')
        derived      = self.think_and_reason()
        alerts       = self.detect_contradictions()
        print(f'  New conclusions: {len(derived)}')
        print(f'  Contradictions:  {len(alerts)}')
        for a in alerts[:5]: print(f'  ! {a}')
        for d in derived[:5]: print(f'  -> {d}')
        print('Deep sleep done.')
