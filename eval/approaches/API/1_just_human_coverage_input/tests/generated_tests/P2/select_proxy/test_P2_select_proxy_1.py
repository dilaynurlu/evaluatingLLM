import pytest
from requests.utils import select_proxy

def test_select_proxy_exact_host_match():
    """
    Test that select_proxy returns the proxy defined specifically for the
    requested scheme and hostname.
    """
    url = "http://example.com/path/to/resource"
    proxies = {
        "http://example.com": "http://10.10.1.10:3128",
        "http": "http://10.10.1.10:8080",
        "all": "socks5://10.10.1.10:1080"
    }
    
    # The function should prioritize the exact scheme://hostname match
    # over the generic scheme or 'all' proxies.
    expected_proxy = "http://10.10.1.10:3128"
    assert select_proxy(url, proxies) == expected_proxy