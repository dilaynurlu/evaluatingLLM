import pytest
from requests.utils import select_proxy

def test_select_proxy_all_fallback_match():
    """
    Test that select_proxy falls back to 'all' when no other specific
    or scheme-based proxies match.
    """
    url = "ftp://ftp.example.com/pub"
    proxies = {
        "http": "http://http-proxy.local:8080",
        "https": "http://https-proxy.local:8080",
        "all": "socks4://global-proxy.local:1080"
    }
    
    # Logic: 
    # ftp://ftp.example.com (missing)
    # ftp (missing)
    # all://ftp.example.com (missing)
    # all (present)
    expected = "socks4://global-proxy.local:1080"
    assert select_proxy(url, proxies) == expected