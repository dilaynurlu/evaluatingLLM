import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies():
    """
    Test that passing None as proxies returns None cleanly.
    """
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None