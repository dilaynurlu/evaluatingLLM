import pytest
from requests.utils import select_proxy

def test_select_proxy_all_specific_host_match():
    """
    Test that select_proxy selects 'all://hostname' when http-specific
    proxies are missing but a host-specific 'all' proxy exists.
    """
    url = "http://specific.example.com/data"
    proxies = {
        "all://specific.example.com": "http://proxy-special.local:8080",
        "all": "http://proxy-catchall.local:8080"
    }
    
    # Logic: 
    # 1. http://specific.example.com (missing)
    # 2. http (missing)
    # 3. all://specific.example.com (present)
    expected = "http://proxy-special.local:8080"
    assert select_proxy(url, proxies) == expected