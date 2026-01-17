import pytest
from requests.utils import select_proxy

def test_select_proxy_all_match():
    """
    Test that select_proxy falls back to the 'all' key if no other keys match.
    """
    url = "gopher://gopher.floodgap.com"
    proxies = {
        "http": "http://http-proxy",
        "https": "http://https-proxy",
        "all": "socks4://general-proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "socks4://general-proxy"