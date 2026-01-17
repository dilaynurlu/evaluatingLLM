import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_host():
    """
    Test that select_proxy correctly constructs keys for IPv6 addresses.
    
    Refinement: Explicitly tests that the proxy key must match the 
    unbracketed IPv6 address, as urlparse strips brackets from the hostname.
    """
    # IPv6 literal in URL usually has brackets
    url = "http://[2001:db8::1]:8080/path"
    
    # The expected key format uses the unbracketed IPv6 address
    proxies = {
        "http://2001:db8::1": "ipv6_proxy",
        "all": "fallback"
    }
    
    assert select_proxy(url, proxies) == "ipv6_proxy"