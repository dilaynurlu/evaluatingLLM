import pytest
from requests.utils import select_proxy

def test_select_proxy_match_all():
    """Test matching 'all' proxy."""
    url = "ftp://example.com/foo"
    proxies = {
        "all": "http://fallback.proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://fallback.proxy"
