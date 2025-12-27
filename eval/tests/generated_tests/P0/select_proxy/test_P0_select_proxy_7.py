import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_all_host_over_all():
    """
    Test that 'all://hostname' takes precedence over 'all'.
    The search order is [scheme://host, scheme, all://host, all].
    """
    url = "http://www.example.com"
    proxies = {
        "all://www.example.com": "http://host-priority.com",
        "all": "http://global-priority.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://host-priority.com"