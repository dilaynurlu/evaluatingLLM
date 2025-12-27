import pytest
from requests.utils import select_proxy

def test_select_proxy_all_host_match():
    """
    Test selecting a proxy defined for 'all://hostname'.
    This key allows defining a proxy for a specific host regardless of scheme,
    or at least behaves as a fallback for specific schemes for that host.
    """
    url = "ftp://ftp.example.com/resource"
    proxies = {
        "all://ftp.example.com": "http://host-proxy.com:8080",
        "all": "http://global-proxy.com:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://host-proxy.com:8080"