import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match():
    """Test when no proxy matches."""
    url = "http://example.com/foo"
    proxies = {
        "https": "https://secure.proxy"
    }
    result = select_proxy(url, proxies)
    assert result is None
