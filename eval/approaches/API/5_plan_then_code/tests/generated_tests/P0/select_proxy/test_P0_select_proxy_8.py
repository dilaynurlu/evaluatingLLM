import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_hostname_formatting():
    """
    Test that select_proxy handles IPv6 addresses by constructing keys 
    without the surrounding brackets (following urllib.parse behavior).
    """
    url = "http://[2001:db8::1]/index.html"
    proxies = {
        # The key constructed is scheme + "://" + hostname (without brackets)
        "http://2001:db8::1": "http://ipv6-proxy.com",
        "http://[2001:db8::1]": "http://bracketed-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://ipv6-proxy.com"