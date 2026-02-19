import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_hostname():
    """
    Test select_proxy with an IPv6 URL. 
    It ensures that the function correctly extracts the hostname without brackets 
    to construct the lookup key (e.g., 'http://::1' instead of 'http://[::1]').
    """
    url = "http://[::1]:8080/index.html"
    proxies = {
        "http://::1": "http://ipv6-proxy",
        "all": "http://global-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://ipv6-proxy"