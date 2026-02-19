import pytest
from requests.utils import select_proxy

def test_select_proxy_match_scheme_host():
    """Test matching scheme://host specific proxy."""
    url = "http://example.com/foo"
    proxies = {
        "http://example.com": "http://proxy.example.com",
        "http": "http://other.proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://proxy.example.com"
