import pytest
from requests.utils import select_proxy

def test_select_proxy_all():
    proxies = {"all": "http://proxy.com"}
    url = "ftp://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
