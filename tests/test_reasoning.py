import sys; sys.path.insert(0, '.')

def test_modus_ponens():
    from ka_mind.framework.model import KaModel
    m = KaModel('ReasonTest', 'logic')
    m.learn(
        'Dogs are animals. '
        'All animals need food. '
        'When animals need food and have no food, they get hungry. '
        'Rex is a dog.'
    )
    result = m.reason('Rex needs food')
    print(f'Modus Ponens: {result}')
    print('PASS  Modus Ponens reasoning')

def test_causal_chain():
    from ka_mind.framework.model import KaModel
    m = KaModel('CausalTest', 'science')
    m.learn(
        'Sun heats water because solar radiation transfers energy. '
        'Water heats because sun shines on it. '
        'When water heats, it evaporates because molecular motion increases. '
        'Evaporation causes clouds because water vapor rises and condenses.'
    )
    chain = m.reasoner.causal_chain('sun shines', depth=4)
    print(f'Causal chain: {chain}')
    print('PASS  Causal chain reasoning')

def test_abduction():
    from ka_mind.framework.model import KaModel
    m = KaModel('AbductTest', 'science')
    m.learn(
        'When it rains, ground gets wet. '
        'When pipes burst, ground gets wet. '
        'Rain causes flooding because water accumulates.'
    )
    explanations = m.why('ground is wet')
    print(f'Abduction (why ground is wet?): {explanations}')
    assert len(explanations) > 0
    print('PASS  Abductive reasoning')

def test_api_sk_detection():
    from ka_mind.agents.api_connector_agent import APIConnectorAgent
    from ka_mind.core.graph_memory import GraphMemory
    a = APIConnectorAgent(GraphMemory())
    # Anthropic should be detected before openai (sk-ant- is more specific)
    detected = a._detect('sk-ant-api12345678901234567890')
    assert detected == 'anthropic', f'Got {detected}, expected anthropic'
    # OpenRouter sk-or- prefix
    detected2 = a._detect('sk-or-api12345678901234567890')
    assert detected2 == 'openrouter', f'Got {detected2}'
    print('PASS  sk- collision fixed (anthropic + openrouter)')

def test_forward_chain():
    from ka_mind.framework.model import KaModel
    m = KaModel('ForwardTest')
    m.learn(
        'If it rains, roads get wet. '
        'If roads are wet, accidents increase. '
        'Rain is falling today.'
    )
    derived = m.reasoner.forward_chain(max_steps=3)
    print(f'Forward chain derived: {derived}')
    print('PASS  Forward chaining')

if __name__ == '__main__':
    print('\nKA-Mind v2.3 Reasoning Tests\n')
    test_modus_ponens()
    test_causal_chain()
    test_abduction()
    test_api_sk_detection()
    test_forward_chain()
    print('\nAll reasoning tests passed!')
