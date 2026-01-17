import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_priority_over_all_host():
    """
    Test that a generic scheme proxy ('https') takes precedence over 
    a specific 'all' proxy ('all://hostname').
    
    Refinement: Uses HTTPS to cover mixed schemes coverage.
    """
    url = "https://example.com/resource"
    proxies = {
        # Missing "https://example.com"
        "https": "https_scheme_proxy",
        "all://example.com": "all_host_proxy",
        "all": "all_proxy",
    }
    
    # Expect match on scheme ('https')
    assert select_proxy(url, proxies) == "https_scheme_proxy"