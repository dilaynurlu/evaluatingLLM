import pytest
from requests.utils import select_proxy

def test_select_proxy_none_argument():
    """
    Test that passing None as the proxies argument is handled gracefully
    (treated as empty dict) and returns None.
    """
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None