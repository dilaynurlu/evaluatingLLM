import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_handling():
    """
    Test that select_proxy correctly handles IPv6 literals in URLs.
    
    The URL parsing logic typically separates the bracketed IPv6 address.
    The proxy key construction expects unbracketed IPv6 addresses for the hostname part.
    """
    # IPv6 address in URL is bracketed
    url = "http://[2001:db8::1]/index.html"
    
    proxies = {
        # Key must be unbracketed IPv6 address
        "http://2001:db8::1": "http://ipv6-proxy",
        "all": "http://fallback-proxy"
    }
    
    # Should match the specific IPv6 key
    expected_proxy = "http://ipv6-proxy"
    assert select_proxy(url, proxies) == expected_proxy