from requests.utils import select_proxy

def test_select_proxy_none_input():
    # Scenario: proxies argument is None.
    # Critique addressed: Robustness.
    # Basic check ensuring no exception is raised.
    url = "http://example.com"
    
    result = select_proxy(url, None)
    
    assert result is None