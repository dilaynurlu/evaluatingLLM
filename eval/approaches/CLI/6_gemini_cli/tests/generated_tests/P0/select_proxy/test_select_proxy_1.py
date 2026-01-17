
import pytest
from requests.utils import select_proxy

def test_select_proxy_exact_match():
    url = "http://example.com"
    proxies = {"http://example.com": "http://proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
