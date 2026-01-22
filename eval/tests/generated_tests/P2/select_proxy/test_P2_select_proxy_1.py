import pytest
from requests.utils import select_proxy

def test_select_proxy_exact_scheme_host_match():
    """
    Test that select_proxy correctly prioritizes an exact match for 
    scheme://hostname over broader proxy definitions.
    """
    url = "http://example.com/resource"
    proxies = {
        "http://example.com": "http://proxy-specific.local:8080",
        "http": "http://proxy-general.local:8080",
        "all": "socks5://proxy-all.local:1080"
    }
    
    # Logic: Should match 'http://example.com' first
    expected = "http://proxy-specific.local:8080"
    assert select_proxy(url, proxies) == expected