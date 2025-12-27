import pytest
from requests.utils import select_proxy

def test_select_proxy_malformed_url_handling():
    """
    Refined test for 'no match' covering Malformed URLs.
    Ensures that a URL with missing authority (empty hostname) does not crash
    the parser and falls back to matching the scheme if valid.
    """
    # URL with scheme but empty host (triple slash)
    url = "http:///some/path"
    
    proxies = {
        # Should match the scheme 'http' even if host is missing/empty
        "http": "http://proxy.general:8080",
        "all://other.com": "other_proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.general:8080"