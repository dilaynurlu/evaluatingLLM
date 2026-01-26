import pytest
from requests.utils import select_proxy

def test_select_proxy_ignores_port_in_lookup():
    """
    Test that the port in the URL is ignored when looking up the proxy.
    The constructed key should use the hostname only.
    """
    url = "http://example.com:8080/resource"
    proxies = {
        "http://example.com": "http://host-only.proxy"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://host-only.proxy"