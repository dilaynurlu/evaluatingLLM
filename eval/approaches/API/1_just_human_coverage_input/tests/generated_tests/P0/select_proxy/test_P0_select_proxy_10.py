import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match_returns_none():
    """
    Test that select_proxy returns None when no matching key is found in the proxies dictionary.
    """
    url = "http://example.com"
    proxies = {
        "https": "https-proxy",
        "ftp": "ftp-proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result is None