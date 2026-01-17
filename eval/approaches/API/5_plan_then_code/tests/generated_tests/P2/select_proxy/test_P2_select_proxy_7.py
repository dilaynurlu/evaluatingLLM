import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_formatting():
    """
    Test select_proxy handling of IPv6 addresses.
    
    The function constructs keys using the hostname. For IPv6, urlparse returns the hostname 
    without brackets. The proxies dictionary must be keyed with the unbracketed IPv6 address 
    to match.
    """
    # URL has IPv6 literal with brackets
    url = "http://[2001:db8::1]/"
    
    # Expected behavior: select_proxy extracts '2001:db8::1' (no brackets)
    # and constructs the key 'http://2001:db8::1'.
    
    proxies = {
        "http://2001:db8::1": "http://ipv6.specific.proxy",
        "http://[2001:db8::1]": "http://bad.key.proxy",  # Should NOT match this
        "all": "http://fallback.proxy"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://ipv6.specific.proxy"