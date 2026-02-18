import pytest
from requests.utils import select_proxy

def test_select_proxy_match_scheme():
    """Test matching scheme specific proxy."""
    url = "http://example.com/foo"
    proxies = {
        "http": "http://proxy.example.com",
        "all": "http://fallback.proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://proxy.example.com"
