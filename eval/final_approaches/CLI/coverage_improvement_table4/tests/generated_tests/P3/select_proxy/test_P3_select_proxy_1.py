import pytest
from requests.utils import select_proxy

def test_select_proxy_exact_match():
    proxies = {
        "http://example.com": "http://proxy.example.com",
        "http": "http://generic.proxy"
    }
    url = "http://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.example.com"
