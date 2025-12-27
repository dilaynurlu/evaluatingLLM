import pytest
from requests.utils import select_proxy

def test_select_proxy_all_match():
    """
    Test selecting a proxy defined for 'all'.
    This is the catch-all proxy when no specific scheme or host matches are found.
    """
    url = "https://www.example.com/resource"
    proxies = {
        "all": "http://catchall-proxy.com:8080",
        "ftp": "http://ftp-proxy.com:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://catchall-proxy.com:8080"