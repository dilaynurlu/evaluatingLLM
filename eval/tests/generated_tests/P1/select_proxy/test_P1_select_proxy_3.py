import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_all_host_match():
    """
    Test that select_proxy prefers the 'all://<hostname>' match when
    specific scheme matches are missing, taking precedence over generic 'all'.
    """
    url = "http://example.com/resource"
    proxies = {
        "all://example.com": "http://priority-three-proxy.com",
        "all": "http://priority-four-proxy.com",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://priority-three-proxy.com"