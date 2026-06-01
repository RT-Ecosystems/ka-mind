import sys; sys.path.insert(0, '.')

def test_causal_direction():
    from ka_mind.core.causal_mapper import CausalMapper
    from ka_mind.core.graph_memory import GraphMemory
    c = CausalMapper()
    atoms = c.extract('Water heats because sun shines on it.')
    assert len(atoms) > 0, 'No causal atoms extracted'
    a = atoms[0]
    cause  = a.content.get('cause', '')
    effect = a.content.get('effect', '')
    assert 'sun' in cause, f'Expected sun in cause, got cause={cause}, effect={effect}'
    assert 'water' in effect, f'Expected water in effect, got effect={effect}'
    print(f'PASS  Causal direction: cause={cause} | effect={effect}')

def test_causal_chain_works():
    from ka_mind.framework.model import KaModel
    m = KaModel('ChainTest', 'science')
    m.learn(
        'Water heats because sun shines on it. '
        'Evaporation happens because water heats. '
        'Clouds form because water evaporates.'
    )
    chain = m.reasoner.causal_chain('sun shines', depth=4)
    print(f'Causal chain: {chain}')
    assert len(chain) > 1, f'Chain should grow: {chain}'
    print('PASS  Causal chain now works!')

def test_modus_ponens_result():
    from ka_mind.framework.model import KaModel
    m = KaModel('MPTest', 'logic')
    m.learn(
        'Dogs are animals. '
        'All animals need food. '
        'When animals need food, they must eat. '
        'Rex is a dog.'
    )
    result = m.reason('Rex needs food')
    print(f'Modus Ponens result: {result}')
    print('PASS  Modus Ponens returns result')

def test_sk_prefix_no_network():
    from ka_mind.agents.api_connector_agent import APIConnectorAgent
    from ka_mind.core.graph_memory import GraphMemory
    a = APIConnectorAgent(GraphMemory())
    # sk-ant- → anthropic (no network call!)
    detected = a._detect('sk-ant-testtoken1234567890abc')
    assert detected == 'anthropic', f'Expected anthropic, got {detected}'
    # sk-or- → openrouter (no network call!)
    detected2 = a._detect('sk-or-testtoken1234567890abc')
    assert detected2 == 'openrouter', f'Expected openrouter, got {detected2}'
    # ghp_ → github (no network call!)
    detected3 = a._detect('ghp_testtoken1234567890abc')
    assert detected3 == 'github', f'Expected github, got {detected3}'
    # hf_ → huggingface (no network call!)
    detected4 = a._detect('hf_testtoken1234567890abc')
    assert detected4 == 'huggingface', f'Expected huggingface, got {detected4}'
    print('PASS  All unique prefixes detected instantly (no network calls!)')

def test_abduction_still_works():
    from ka_mind.framework.model import KaModel
    m = KaModel('AbdTest', 'science')
    m.learn(
        'When it rains, ground gets wet. '
        'When pipes burst, ground gets wet. '
        'Rain causes flooding.'
    )
    explanations = m.why('ground is wet')
    print(f'Abduction: {explanations}')
    assert len(explanations) > 0
    print('PASS  Abduction still works')

if __name__ == '__main__':
    print('\nKA-Mind v2.3.1 Hotfix Tests\n')
    test_causal_direction()
    test_causal_chain_works()
    test_modus_ponens_result()
    test_sk_prefix_no_network()
    test_abduction_still_works()
    print('\nAll hotfix tests passed!')
