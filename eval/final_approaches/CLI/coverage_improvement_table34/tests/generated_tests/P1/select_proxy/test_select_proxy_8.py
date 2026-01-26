import pytest
from requests.utils import select_proxy

def test_select_proxy_empty_proxies():
    """Test with empty proxies dict."""
    url = "http://example.com"
    result = select_proxy(url, {})
    assert result is None
