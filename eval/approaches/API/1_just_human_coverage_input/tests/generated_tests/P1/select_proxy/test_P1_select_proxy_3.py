import pytest
from requests.utils import select_proxy

def test_select_proxy_all_host_priority_over_all():
    """
    Test that a proxy defined for 'all://hostname' takes precedence
    over a generic 'all' proxy.
    """
    url = "ftp://files.example.com/upload"
    proxies = {
        "all://files.example.com": "http://host-proxy.local:3128",
        "all": "http://generic-all.local:8080"
    }
    
    # Expected: 'all://files.example.com' comes before 'all' in the lookup order
    result = select_proxy(url, proxies)
    assert result == "http://host-proxy.local:3128"