import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallback_all():
    """
    Test selecting a proxy when the URL has no hostname and the specific scheme is missing.
    The function should fallback to the 'all' key.
    """
    url = "mailto:user@example.com"
    proxies = {
        "http": "http://http-proxy.com",
        "all": "http://fallback-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://fallback-proxy.com"