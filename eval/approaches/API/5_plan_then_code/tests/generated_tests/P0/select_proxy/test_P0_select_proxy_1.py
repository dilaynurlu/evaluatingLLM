import pytest
from requests.utils import select_proxy

def test_select_proxy_matches_scheme():
    """
    Test that select_proxy correctly identifies and returns the proxy 
    corresponding to the URL scheme when a specific host match is not present.
    """
    url = "http://example.com/resource"
    proxies = {
        "http": "http://proxy.example.com:8080",
        "https": "http://secure.example.com:8443"
    }
    
    # Should match 'http' key
    result = select_proxy(url, proxies)
    assert result == "http://proxy.example.com:8080"