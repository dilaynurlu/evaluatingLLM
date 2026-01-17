import pytest
from requests.utils import select_proxy

def test_select_proxy_with_port_ignored_in_key():
    """
    Test that the port in the URL is ignored when looking up keys in the proxies dictionary.
    The function constructs keys using hostname, not netloc.
    """
    url = "http://example.com:8080/api"
    
    # If the port was included, the key would be 'http://example.com:8080'
    # But select_proxy uses 'http://example.com'
    proxies = {
        "http://example.com": "proxy-found",
        "http://example.com:8080": "proxy-not-used"
    }
    
    result = select_proxy(url, proxies)
    assert result == "proxy-found"