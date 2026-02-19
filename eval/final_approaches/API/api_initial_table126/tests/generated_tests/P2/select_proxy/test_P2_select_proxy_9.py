import pytest
from requests.utils import select_proxy

def test_select_proxy_ignore_port_in_key():
    """
    Test that the presence of a port in the URL does not prevent matching
    against a proxy key defined by scheme and hostname (without port).
    """
    url = "https://secure.example.com:8443/resource"
    proxies = {
        "https://secure.example.com": "http://secure-proxy.local",
        "https": "http://general-proxy.local"
    }
    
    # Logic:
    # urlparse extracts hostname 'secure.example.com' (port is separate)
    # Key constructed: 'https://secure.example.com'
    expected = "http://secure-proxy.local"
    assert select_proxy(url, proxies) == expected