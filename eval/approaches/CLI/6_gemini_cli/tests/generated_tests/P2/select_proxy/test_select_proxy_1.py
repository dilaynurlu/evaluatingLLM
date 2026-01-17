import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_host():
    proxies = {
        "http://example.com": "http://proxy.com",
        "http": "http://other.com"
    }
    url = "http://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
