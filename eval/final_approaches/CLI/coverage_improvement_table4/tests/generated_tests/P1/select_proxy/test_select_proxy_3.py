import pytest
from requests.utils import select_proxy

def test_select_proxy_match_all_host():
    """Test matching all://host specific proxy."""
    url = "ftp://example.com/foo"
    proxies = {
        "all://example.com": "http://proxy.example.com",
        "all": "http://fallback.proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://proxy.example.com"
