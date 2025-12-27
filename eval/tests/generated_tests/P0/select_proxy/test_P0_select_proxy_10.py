import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_no_match():
    """
    Test selecting a proxy when the URL has no hostname and neither scheme nor 'all' is present.
    It should return None.
    """
    url = "mailto:user@example.com"
    proxies = {
        "http": "http://http-proxy.com",
        "https": "http://https-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result is None