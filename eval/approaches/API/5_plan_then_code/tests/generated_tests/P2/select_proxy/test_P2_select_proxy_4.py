import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_all_match():
    """
    Test that select_proxy falls back to 'all' if no other specific keys match.
    
    Given a URL 'http://example.com/foo'
    And a proxies dictionary containing only:
      - 'all' (Generic)
    
    The function should return the value for 'all'.
    """
    url = "http://example.com/path"
    proxies = {
        "all": "http://proxy.generic:8080",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.generic:8080"