import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_all_match():
    """
    Test proxy selection for a URL without a hostname (e.g. file:// scheme)
    falling back to 'all' when the scheme is not in proxies.
    """
    url = "file:///tmp/test.txt"
    proxies = {
        "http": "http-proxy",
        "all": "catch-all-proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "catch-all-proxy"