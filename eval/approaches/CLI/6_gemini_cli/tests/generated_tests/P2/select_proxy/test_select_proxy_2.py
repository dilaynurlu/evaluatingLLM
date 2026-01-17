import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme():
    proxies = {
        "http": "http://proxy.com"
    }
    url = "http://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
