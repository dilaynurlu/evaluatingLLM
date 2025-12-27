import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match_returns_none():
    """
    Test that select_proxy returns None when a valid proxies dictionary is provided
    but contains no matching keys for the given URL.
    """
    url = "http://example.com"
    proxies = {
        "https": "http://secure-proxy.com",
        "ftp": "http://ftp-proxy.com",
        "all://other.com": "http://other-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result is None