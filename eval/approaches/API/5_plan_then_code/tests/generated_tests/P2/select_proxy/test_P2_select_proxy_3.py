import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_all_host_match():
    """
    Test that select_proxy falls back to all://<host> if specific scheme matches are missing.
    
    Given a URL 'http://example.com/foo'
    And a proxies dictionary containing keys for:
      - 'all://example.com' (All + Host)
      - 'all' (Generic)
    
    The function should return the value for 'all://example.com'.
    """
    url = "http://example.com/path"
    proxies = {
        "all://example.com": "http://proxy.all.host:8080",
        "all": "http://proxy.generic:8080",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.all.host:8080"