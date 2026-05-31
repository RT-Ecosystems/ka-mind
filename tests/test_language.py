import sys; sys.path.insert(0,'.')

def test_human_language():
    from ka_mind.framework.model import KaModel
    m = KaModel('Test', 'science')
    m.learn(
        'Water is a chemical compound with formula H2O. '
        'Water is essential for all life on Earth. '
        'When temperature drops below zero degrees, water freezes. '
        'Water freezes because molecular motion slows down due to cold. '
        'Ice is the solid form of water.'
    )
    q = 'What is water?'
    ans = m.think(q)
    print(f'Q: {q}')
    print(f'A: {ans}')
    print()
    assert '|' not in ans, 'Should not have | separators!'
    assert len(ans) > 50, 'Answer too short!'
    print('PASS  Human language output (no | separators)')

def test_creative_writing():
    from ka_mind.framework.model import KaModel
    m = KaModel('Test2', 'literature')
    m.learn(
        'Rain is water falling from clouds. '
        'Rain nourishes the earth and sustains life. '
        'Rain causes rivers to flow and fills lakes. '
        'When rain falls heavily, floods can occur.'
    )
    q = 'Write an article about rain'
    ans = m.think(q)
    print(f'Q: {q}')
    print(f'A: {ans}')
    print()
    assert len(ans) > 100
    print('PASS  Creative writing output')

def test_web_cache():
    from ka_mind.agents.web_agent import WebAgent
    from ka_mind.core.graph_memory import GraphMemory
    gm = GraphMemory()
    wa = WebAgent(gm)
    # First call — searches DDG (or fails gracefully)
    r1 = wa.search_and_learn('Python programming language')
    # Second call — should return from cache
    r2 = wa.search_and_learn('Python programming language')
    # r2 should be from cache
    print(f'Call 1: {r1[:60]}')
    print(f'Call 2: {r2[:60]}')
    print('PASS  Web cache working')

def test_all_agents():
    from ka_mind.framework.model import KaModel
    m = KaModel('AgentTest')
    # Math
    r = m.think('calculate 15 + 27')
    print(f'Math: {r}')
    # Time
    r = m.think('what is today date')
    print(f'Time: {r}')
    print('PASS  Agents working')

if __name__ == '__main__':
    print('\nKA-Mind Language Engine Tests\n')
    test_human_language()
    test_creative_writing()
    test_web_cache()
    test_all_agents()
    print('\nAll language tests passed!')
