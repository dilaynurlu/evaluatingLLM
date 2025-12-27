import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_specific_host():
    """
    Test that specific scheme://hostname proxy takes precedence over 
    scheme-only, all://hostname, and 'all' proxies.
    
    The expected order of precedence for a URL like scheme://host is:
    1. scheme://host
    2. scheme
    3. all://host
    4. all
    """
    url = "http://example.com/api/resource"
    proxies = {
        "http://example.com": "http://specific-host-proxy.local:8080",
        "http": "http://scheme-proxy.local:8080",
        "all://example.com": "http://all-host-proxy.local:8080",
        "all": "http://catch-all-proxy.local:8080",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://specific-host-proxy.local:8080"