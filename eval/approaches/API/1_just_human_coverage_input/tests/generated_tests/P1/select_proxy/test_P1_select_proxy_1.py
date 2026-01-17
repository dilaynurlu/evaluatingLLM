import pytest
from requests.utils import select_proxy

def test_select_proxy_specific_host_priority():
    """
    Test that a proxy defined for a specific scheme+hostname takes precedence
    over a generic scheme proxy.
    """
    url = "http://example.com/api"
    proxies = {
        "http://example.com": "http://priority-proxy.local:3128",
        "http": "http://generic-proxy.local:8080",
        "all": "http://fallback.local:80"
    }
    
    # Expected: The specific 'http://example.com' key matches first
    result = select_proxy(url, proxies)
    assert result == "http://priority-proxy.local:3128"