import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallback():
    """
    Test that URLs without a hostname fall back to 'all' if their
    specific scheme is not in the proxies dictionary.
    """
    url = "file:///var/log/syslog"
    proxies = {
        "http": "http://http-proxy.local",
        "all": "http://fallback-proxy.local"
    }
    
    # Logic for no hostname:
    # Check 'file' (missing) -> fallback to 'all'
    expected = "http://fallback-proxy.local"
    assert select_proxy(url, proxies) == expected