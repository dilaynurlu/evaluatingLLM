import pytest
from requests.utils import select_proxy

def test_select_proxy_explicit_none_value_returns_none():
    """
    Test that if a matching proxy key has a value of None, the function returns None.
    This pattern is used to explicitly bypass proxies for certain hosts.
    """
    url = "http://internal.example.com"
    proxies = {
        "http://internal.example.com": None,
        "all": "http://gateway.proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result is None