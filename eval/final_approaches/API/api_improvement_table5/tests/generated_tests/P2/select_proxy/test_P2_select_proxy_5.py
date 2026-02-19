import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_specific_host():
    """
    Test the highest priority match: scheme://hostname.
    It should take precedence over scheme-only, all://hostname, and all.
    """
    url = "http://example.com/resource"
    proxies = {
        "http://example.com": "http://specific-host.proxy",
        "http": "http://scheme.proxy",
        "all://example.com": "http://all-host.proxy",
        "all": "http://all.proxy",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://specific-host.proxy"