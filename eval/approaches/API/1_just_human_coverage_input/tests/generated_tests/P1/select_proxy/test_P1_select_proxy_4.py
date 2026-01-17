import pytest
from requests.utils import select_proxy

def test_select_proxy_fallback_to_all():
    """
    Test that the function falls back to the 'all' key if no other
    specific keys match.
    """
    url = "http://unknown-host.com/resource"
    proxies = {
        "https": "http://secure-proxy.local:8443",
        "all": "socks5://fallback-proxy.local:9000"
    }
    
    # Expected: No scheme match (http != https), no host match, fallback to 'all'
    result = select_proxy(url, proxies)
    assert result == "socks5://fallback-proxy.local:9000"