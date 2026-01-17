import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_fallback():
    """
    Test that select_proxy falls back to a generic scheme proxy
    when no specific hostname match is found.
    """
    url = "https://example.org/secure"
    proxies = {
        "http": "http://insecure-proxy.local",
        "https": "http://secure-proxy.local",
        "all": "socks5://fallback-proxy.local"
    }
    
    # 'https://example.org' is not in proxies, so it should match 'https'
    expected_proxy = "http://secure-proxy.local"
    assert select_proxy(url, proxies) == expected_proxy