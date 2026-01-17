import pytest
from requests.utils import select_proxy

def test_select_proxy_exact_host_match():
    """
    Test that select_proxy prefers a proxy defined specifically for 
    the 'scheme://hostname' key over others.
    """
    url = "http://example.com/some/path"
    proxies = {
        "http://example.com": "http://special-proxy.example.com:8080",
        "http": "http://generic-proxy.example.com:8080",
        "all": "socks5://fallback-proxy:1080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://special-proxy.example.com:8080"