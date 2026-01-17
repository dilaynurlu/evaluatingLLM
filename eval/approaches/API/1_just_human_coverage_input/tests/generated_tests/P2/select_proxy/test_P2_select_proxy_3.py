import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_scheme_over_all_host():
    """
    Test the precedence logic where a generic scheme proxy takes priority
    over a host-specific 'all' proxy.
    
    Based on the implementation, the search order is:
    1. scheme://hostname
    2. scheme
    3. all://hostname
    4. all
    """
    url = "http://example.com"
    proxies = {
        # This corresponds to key 'http' (index 1 in search list)
        "http": "http://scheme-generic-proxy",
        
        # This corresponds to key 'all://example.com' (index 2 in search list)
        "all://example.com": "http://host-specific-all-proxy",
        
        # This corresponds to key 'all' (index 3 in search list)
        "all": "http://catch-all-proxy"
    }
    
    # We expect 'http' to be selected before 'all://example.com'
    expected_proxy = "http://scheme-generic-proxy"
    assert select_proxy(url, proxies) == expected_proxy