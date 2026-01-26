import pytest
from requests.utils import select_proxy

def test_select_proxy_returns_none_when_no_match_found():
    """Test that select_proxy returns None when proxies are provided but no match is found."""
    url = "http://example.com"
    proxies = {
        "https": "https://secure.proxy",
        "ftp://example.com": "ftp://ftp.proxy"
    }
    
    result = select_proxy(url, proxies)
    
    assert result is None