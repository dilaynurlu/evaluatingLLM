import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies_arg():
    """
    Test that passing None as the proxies argument is handled gracefully.
    The function should treat it as an empty dictionary and return None
    (as no proxy can be found).
    """
    url = "http://example.com"
    proxies = None
    
    result = select_proxy(url, proxies)
    
    assert result is None