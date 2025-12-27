import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_exact_match():
    """
    Test that select_proxy prefers the exact '<scheme>://<hostname>' match
    over broader matches like '<scheme>', 'all://<hostname>', or 'all'.
    """
    url = "http://example.com/resource"
    proxies = {
        "http://example.com": "http://priority-one-proxy.com",
        "http": "http://priority-two-proxy.com",
        "all://example.com": "http://priority-three-proxy.com",
        "all": "http://priority-four-proxy.com",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://priority-one-proxy.com"