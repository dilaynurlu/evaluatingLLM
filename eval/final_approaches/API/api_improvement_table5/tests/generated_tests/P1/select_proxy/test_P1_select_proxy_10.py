import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match_returns_none():
    """
    Test that select_proxy returns None when a proxies dictionary is provided,
    but none of the generated keys match any entry in the dictionary.
    """
    url = "ftp://example.com/resource"
    proxies = {
        "http": "http-proxy",
        "https": "https-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result is None