import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies_arg():
    """
    Test that select_proxy gracefully handles None as the proxies argument
    and returns None.
    """
    url = "http://example.com"
    proxies = None
    
    # Logic:
    # proxies = proxies or {} -> {}
    # No keys match empty dict
    assert select_proxy(url, proxies) is None