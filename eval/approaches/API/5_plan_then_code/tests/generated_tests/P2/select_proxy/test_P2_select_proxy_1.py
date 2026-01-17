import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_full_match():
    """
    Test that select_proxy prioritizes the most specific match: <scheme>://<host>.
    
    Given a URL 'http://example.com/foo'
    And a proxies dictionary containing keys for:
      - 'http://example.com' (Specific Scheme + Host)
      - 'http' (Scheme only)
      - 'all://example.com' (All + Host)
      - 'all' (Generic)
    
    The function should return the value for 'http://example.com'.
    """
    url = "http://example.com/path"
    proxies = {
        "http://example.com": "http://proxy.specific.host:8080",
        "http": "http://proxy.scheme:8080",
        "all://example.com": "http://proxy.all.host:8080",
        "all": "http://proxy.generic:8080",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.specific.host:8080"