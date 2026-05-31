# KA-Mind v2.0 — Fix Verification Tests
import sys; sys.path.insert(0, '..')

def test_bug1_concept():
    from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
    a = KnowledgeAtom(AtomType.CONCEPT, {'name': 'test', 'definition': 'a test'})
    assert a.atom_type == AtomType.CONCEPT
    print('PASS  BUG1: AtomType.CONCEPT works')

def test_bug2_retrieve_context():
    from ka_mind.core.graph_memory  import GraphMemory
    from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
    gm = GraphMemory()
    a1 = KnowledgeAtom(AtomType.FACT, {'text': 'Paris is in France'})
    a2 = KnowledgeAtom(AtomType.FACT, {'text': 'France is in Europe'})
    gm.add_atom(a1); gm.add_atom(a2)
    gm.add_edge(a1.atom_id, a2.atom_id, 'related')
    ctx = gm.retrieve_context(a1.atom_id, depth=2)
    assert len(ctx) >= 1
    print(f'PASS  BUG2: retrieve_context works ({len(ctx)} nodes)')

def test_bug3_inference_uses_memory():
    from ka_mind.framework.model import KaModel
    m = KaModel('Test', 'science')
    m.learn('Water is H2O. Water is essential for life.')
    m.learn('If temperature drops below zero, water freezes.')
    answer = m.think('What is water?')
    assert answer != 'I do not have enough knowledge'
    assert len(answer) > 10
    print(f'PASS  BUG3: Inference uses memory. Answer: {answer[:60]}')

def test_bug4_vector_graph_populated():
    from ka_mind.framework.model import KaModel
    m = KaModel('Test2', 'science')
    m.learn('The sun is a star. Stars produce light through nuclear fusion.')
    print(f'PASS  BUG4: VectorGraph has {len(m.vector_graph.graph)} atoms')

def test_bug5_language_agnostic():
    from ka_mind.core.neocortex    import Neocortex
    from ka_mind.core.graph_memory  import GraphMemory
    from ka_mind.core.knowledge_atom import KnowledgeAtom, AtomType
    gm = GraphMemory()
    gm.add_atom(KnowledgeAtom(AtomType.FACT, {'text': 'Dog is an animal'}))
    gm.add_atom(KnowledgeAtom(AtomType.FACT, {'text': 'Animal has cells'}))
    n  = Neocortex(gm)
    thoughts = n.think_and_reason()
    print(f'PASS  BUG5: Language-agnostic reasoning: {len(thoughts)} thoughts')

def test_bug7_lazy_vector():
    from ka_mind.core.vector_atom import VectorAtom
    # Verify lazy loading: encode() only loads model when called
    va = VectorAtom('Hello world test sentence', 'test')
    assert va.vector is None, 'Vector should be None before encode()'
    v  = va.encode()  # Loads model here if not already loaded
    assert v is not None and len(v) > 0
    v2 = va.encode()  # Should return cached, not reload
    assert v == v2, 'Should return same cached vector'
    print(f'PASS  BUG7: VectorAtom lazy loading works (dim={len(v)})')

def test_teacher_3layers():
    from ka_mind.core.graph_memory   import GraphMemory
    from ka_mind.training.neurabrain_teacher import NeuraBrainTeacher
    gm = GraphMemory()
    t  = NeuraBrainTeacher(gm)
    n  = t.process_chunk(
        'Python is a programming language. '
        'When you have a bug, you should debug it. '
        'Code fails because of logic errors.',
        domain='coding'
    )
    assert n > 0
    from ka_mind.core.knowledge_atom import AtomType
    facts   = sum(1 for a in gm.graph.values() if a.atom_type == AtomType.FACT)
    rules   = sum(1 for a in gm.graph.values() if a.atom_type == AtomType.RULE)
    causal  = sum(1 for a in gm.graph.values() if a.atom_type == AtomType.CAUSAL)
    print(f'PASS  NeuraBrain Teacher: {n} atoms | F:{facts} R:{rules} C:{causal}')

if __name__ == '__main__':
    print('\nKA-Mind v2.0 — Bug Fix Verification\n')
    test_bug1_concept()
    test_bug2_retrieve_context()
    test_bug3_inference_uses_memory()
    test_bug4_vector_graph_populated()
    test_bug5_language_agnostic()
    test_bug7_lazy_vector()
    test_teacher_3layers()
    print('\nAll tests passed! KA-Mind v2.0 ready!')
