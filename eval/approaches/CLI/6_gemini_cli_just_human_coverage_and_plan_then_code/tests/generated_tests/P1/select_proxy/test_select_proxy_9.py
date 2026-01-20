import pytest
from requests.utils import select_proxy

def test_select_proxy_casing():
    proxies = {"http://example.com": "http://proxy.com"}
    url = "HTTP://EXAMPLE.COM/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
