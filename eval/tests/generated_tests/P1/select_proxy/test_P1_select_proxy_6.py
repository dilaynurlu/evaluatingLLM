import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallback():
    """
    Test select_proxy with a URL that has no hostname (e.g., mailto:)
    when the scheme is not in proxies. It should fall back to 'all'.
    """
    url = "mailto:user@example.com"
    proxies = {
        "http": "http://http-proxy.com",
        "all": "http://fallback-proxy.com",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://fallback-proxy.com"