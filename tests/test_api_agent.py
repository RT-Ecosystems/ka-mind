import sys; sys.path.insert(0, '.')

def test_api_detection():
    from ka_mind.agents.api_connector_agent import APIConnectorAgent
    from ka_mind.core.graph_memory import GraphMemory
    agent = APIConnectorAgent(GraphMemory())
    # GitHub prefix detection
    detected = agent._detect_by_prefix('ghp_testtoken12345')
    assert detected == 'github', f'Expected github, got {detected}'
    # OpenAI prefix detection
    detected = agent._detect_by_prefix('sk-testtoken12345abc')
    assert detected == 'openai', f'Expected openai, got {detected}'
    # Slack prefix detection
    detected = agent._detect_by_prefix('xoxb-testtoken12345')
    assert detected == 'slack', f'Expected slack, got {detected}'
    # HuggingFace prefix detection
    detected = agent._detect_by_prefix('hf_testtoken12345abc')
    assert detected == 'huggingface', f'Expected huggingface, got {detected}'
    # Notion prefix detection
    detected = agent._detect_by_prefix('secret_testtoken12345abc')
    assert detected == 'notion', f'Expected notion, got {detected}'
    print('PASS  API prefix auto-detection (github, openai, slack, hf, notion)')

def test_help_message():
    from ka_mind.agents.api_connector_agent import APIConnectorAgent
    from ka_mind.core.graph_memory import GraphMemory
    agent = APIConnectorAgent(GraphMemory())
    help_msg = agent._help_message()
    assert 'github' in help_msg.lower()
    assert 'Usage' in help_msg or 'usage' in help_msg.lower()
    print('PASS  Help message works')

def test_list_connected_empty():
    from ka_mind.agents.api_connector_agent import APIConnectorAgent
    from ka_mind.core.graph_memory import GraphMemory
    agent = APIConnectorAgent(GraphMemory())
    result = agent.list_connected()
    assert 'No APIs' in result
    print('PASS  Empty API list works')

def test_intent_api():
    from ka_mind.framework.model import KaModel
    m = KaModel('APITest')
    intent = m.teacher._intent('connect github api ghp_mytoken')
    assert intent == 'api_connect', f'Expected api_connect, got {intent}'
    intent2 = m.teacher._intent('add api key sk-openai123')
    assert intent2 == 'api_connect'
    print('PASS  API intent detection')

def test_math_fix():
    from ka_mind.framework.model import KaModel
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        m = KaModel('MathTest')
        r = m.think('calculate 25 + 17')
        syntax_warns = [x for x in w if 'escape' in str(x.message).lower()]
        assert len(syntax_warns) == 0, 'Still has escape warning!'
    assert '42' in r, f'Expected 42, got: {r}'
    print(f'PASS  \\d SyntaxWarning FIXED. Math result: {r}')

if __name__ == '__main__':
    print('\nKA-Mind v2.2 Tests\n')
    test_api_detection()
    test_help_message()
    test_list_connected_empty()
    test_intent_api()
    test_math_fix()
    print('\nAll v2.2 tests passed!')
