import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match():
    proxies = {
        "https": "http://secure.proxy"
    }
    url = "http://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy is None
