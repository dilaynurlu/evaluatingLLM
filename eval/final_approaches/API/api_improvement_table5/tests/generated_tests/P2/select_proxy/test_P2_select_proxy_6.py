import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_scheme():
    """
    Test the second priority match: scheme.
    It should take precedence over all://hostname and all, 
    when scheme://hostname is missing.
    """
    url = "http://example.com/resource"
    proxies = {
        "http": "http://scheme.proxy",
        "all://example.com": "http://all-host.proxy",
        "all": "http://all.proxy",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://scheme.proxy"