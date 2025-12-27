import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_scheme_over_all_host():
    """
    Test that a 'scheme' proxy key takes precedence over 'all://hostname'.
    The search order is [scheme://host, scheme, all://host, all].
    """
    url = "http://www.example.com"
    proxies = {
        "http": "http://scheme-priority.com",
        "all://www.example.com": "http://host-priority.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://scheme-priority.com"