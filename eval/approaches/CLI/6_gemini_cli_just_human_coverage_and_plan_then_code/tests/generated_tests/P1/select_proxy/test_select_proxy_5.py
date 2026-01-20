import pytest
from requests.utils import select_proxy

def test_select_proxy_none():
    proxies = None
    url = "http://example.com"
    proxy = select_proxy(url, proxies)
    assert proxy is None
