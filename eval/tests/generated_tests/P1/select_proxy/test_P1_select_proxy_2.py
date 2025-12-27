import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_scheme_match():
    """
    Test that select_proxy prefers the '<scheme>' match when the exact 
    host match is missing, taking precedence over 'all://<hostname>' and 'all'.
    """
    url = "http://example.com/resource"
    proxies = {
        "http": "http://priority-two-proxy.com",
        "all://example.com": "http://priority-three-proxy.com",
        "all": "http://priority-four-proxy.com",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://priority-two-proxy.com"