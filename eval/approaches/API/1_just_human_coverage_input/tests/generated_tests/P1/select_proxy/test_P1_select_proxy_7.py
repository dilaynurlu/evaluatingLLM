import pytest
from requests.utils import select_proxy

def test_select_proxy_ignores_port_in_key_lookup():
    """
    Test that the proxy selection logic uses the hostname without the port
    when constructing lookup keys.
    """
    url = "http://example.com:8080/data"
    proxies = {
        # This key should NOT match because select_proxy uses urlparts.hostname
        "http://example.com:8080": "http://bad-proxy",
        # This key SHOULD match
        "http://example.com": "http://good-proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://good-proxy"