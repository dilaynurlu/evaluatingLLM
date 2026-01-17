
import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match():
    url = "http://example.com"
    proxies = {"https": "http://secure-proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy is None
