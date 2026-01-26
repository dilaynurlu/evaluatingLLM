import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_handling():
    """
    Test that select_proxy correctly constructs keys for IPv6 addresses.
    The key should contain the unbracketed IPv6 address as the hostname.
    """
    # URL uses bracketed IPv6
    url = "http://[2001:db8::1]/path"
    
    # Proxy dict must use unbracketed IPv6 for the key to match
    proxies = {
        "http://2001:db8::1": "http://ipv6.proxy"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://ipv6.proxy"