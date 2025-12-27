import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match_found():
    """
    Test that None is returned when proxies are provided but none match the URL criteria.
    """
    url = "http://www.example.com"
    proxies = {
        "https": "http://secure-proxy.com",
        "ftp": "http://ftp-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result is None