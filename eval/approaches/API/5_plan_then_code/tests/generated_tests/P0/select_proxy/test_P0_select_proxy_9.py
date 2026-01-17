import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies_returns_none():
    """
    Test that select_proxy returns None gracefully when the proxies argument is None.
    """
    url = "http://example.com"
    proxies = None
    
    result = select_proxy(url, proxies)
    assert result is None