import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_fallback():
    """
    Test that if the specific host proxy (scheme://host) is missing, 
    the function correctly falls back to the generic scheme proxy key.
    This also verifies it ignores 'all' proxies if a scheme match exists.
    """
    url = "https://example.com/secure"
    proxies = {
        "https": "http://secure-proxy.local:3128",
        "all://example.com": "http://all-host-proxy.local:3128",
        "all": "http://catch-all.local:3128",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://secure-proxy.local:3128"