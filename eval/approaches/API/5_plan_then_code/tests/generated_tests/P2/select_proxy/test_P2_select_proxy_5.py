import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies():
    """
    Test that select_proxy handles a None value for the proxies argument gracefully.
    
    It should interpret None as an empty set of proxies and return None.
    """
    url = "http://example.com"
    proxies = None
    
    result = select_proxy(url, proxies)
    
    assert result is None