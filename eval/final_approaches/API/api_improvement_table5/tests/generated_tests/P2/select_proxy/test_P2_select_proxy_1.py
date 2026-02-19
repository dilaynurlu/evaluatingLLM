import pytest
from requests.utils import select_proxy

def test_select_proxy_returns_none_when_proxies_is_none():
    """Test that select_proxy returns None if the proxies argument is None."""
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None