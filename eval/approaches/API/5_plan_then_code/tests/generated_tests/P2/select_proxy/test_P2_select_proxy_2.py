import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_scheme_match():
    """
    Test that select_proxy falls back to <scheme> match if <scheme>://<host> is missing.
    
    Given a URL 'http://example.com/foo'
    And a proxies dictionary containing keys for:
      - 'http' (Scheme only)
      - 'all://example.com' (All + Host)
      - 'all' (Generic)
    
    The function should return the value for 'http'.
    """
    url = "http://example.com/path"
    proxies = {
        "http": "http://proxy.scheme:8080",
        "all://example.com": "http://proxy.all.host:8080",
        "all": "http://proxy.generic:8080",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.scheme:8080"