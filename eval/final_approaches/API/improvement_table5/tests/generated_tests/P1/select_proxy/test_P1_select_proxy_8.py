import pytest
from requests.utils import select_proxy

def test_select_proxy_handles_none_proxies():
    """
    Test that select_proxy safely handles a None value for the proxies argument,
    treating it as an empty dictionary and returning None.
    """
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None