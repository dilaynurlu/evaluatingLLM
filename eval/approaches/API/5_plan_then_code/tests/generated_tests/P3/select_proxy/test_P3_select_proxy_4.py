import pytest
from requests.utils import select_proxy

def test_select_proxy_all_fallback():
    """
    Test that select_proxy falls back to 'all' if no other specific keys match
    for a URL with a hostname.
    
    Refinement: Uses a URL with a specific port to verify that the port is ignored
    during hostname matching, ensuring robust fallback.
    """
    # URL with a specific port
    url = "http://example.com:8080/resource"
    proxies = {
        "https": "secure_proxy",
        "all": "generic_proxy",
    }
    
    # 'http' scheme matches nothing specific, should fall back to 'all'
    # The port 8080 should not prevent matching if logic uses hostname
    assert select_proxy(url, proxies) == "generic_proxy"