import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_uses_scheme():
    """
    Test that URLs without a hostname (e.g., file:///) use the scheme 
    to look up the proxy, bypassing host-based keys.
    """
    # file:/// paths result in hostname=None in standard urlparse
    url = "file:///etc/hosts"
    proxies = {
        "file": "http://file-proxy.local",
        "all": "http://catch-all.proxy"
    }
    
    # Should look up 'file' since hostname is None
    result = select_proxy(url, proxies)
    assert result == "http://file-proxy.local"