import pytest
from requests.utils import select_proxy

def test_select_proxy_explicit_none_value():
    """
    Test that if a proxy key exists but its value is None (e.g. explicitly disabled),
    the function returns None (the value) rather than falling back or erroring.
    """
    url = "http://example.com"
    proxies = {
        "http": None,
        "all": "http://fallback-proxy.local:8080"
    }
    
    # 'http' matches, value is None. Should stop and return None.
    result = select_proxy(url, proxies)
    assert result is None