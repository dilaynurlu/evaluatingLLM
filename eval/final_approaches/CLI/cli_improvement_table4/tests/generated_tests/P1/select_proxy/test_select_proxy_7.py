import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies():
    """Test with None proxies dict."""
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None
