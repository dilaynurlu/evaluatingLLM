import pytest
from requests.utils import select_proxy

def test_select_proxy_ignore_port():
    """
    Test that select_proxy ignores the port number in the URL when constructing
    proxy lookup keys.
    """
    # URL contains a port
    url = "http://example.com:8080/api"
    
    # Proxies dict keys should not contain ports to be matched by select_proxy
    proxies = {
        "http://example.com": "http://correct-proxy",
        "http://example.com:8080": "http://wrong-key-proxy"
    }
    
    # The function constructs 'http://example.com' as the key, ignoring :8080.
    # Therefore it should match the entry without the port.
    expected_proxy = "http://correct-proxy"
    assert select_proxy(url, proxies) == expected_proxy