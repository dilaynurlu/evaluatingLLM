import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_host_match():
    """
    Test that select_proxy correctly handles IPv6 literals in the URL.
    The proxy key for an IPv6 host must be the unbracketed address.
    """
    # URL has brackets
    url = "http://[2001:db8::1]/index.html"
    
    # Proxies key must NOT have brackets for exact host match
    # because urlparse strips brackets from hostname.
    proxies = {
        "http://2001:db8::1": "http://ipv6-specific.local",
        "http": "http://ipv6-general.local"
    }
    
    # Logic:
    # Hostname parsed as '2001:db8::1'
    # Key check: 'http://2001:db8::1'
    expected = "http://ipv6-specific.local"
    assert select_proxy(url, proxies) == expected