import pytest
from requests.utils import select_proxy

def test_select_proxy_auth_and_port_stripping():
    """
    Test that select_proxy ignores authentication information and port numbers
    when constructing the lookup key for the proxy dictionary.
    """
    # URL includes user:pass and port 8080
    url = "http://user:pass@example.com:8080/path"
    
    # The key constructed should be 'http://example.com'
    # It should NOT include user:pass or :8080
    
    proxies = {
        "http://example.com": "http://clean.host.proxy",
        "http://user:pass@example.com": "http://auth.included.proxy",
        "http://example.com:8080": "http://port.included.proxy"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://clean.host.proxy"