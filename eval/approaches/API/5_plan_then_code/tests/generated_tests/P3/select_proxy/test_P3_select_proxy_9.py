import pytest
from requests.utils import select_proxy

def test_select_proxy_none_argument():
    """
    Test that select_proxy handles None for the proxies argument gracefully,
    treating it as an empty dict and returning None.
    """
    url = "http://example.com"
    proxies = None
    
    assert select_proxy(url, proxies) is None