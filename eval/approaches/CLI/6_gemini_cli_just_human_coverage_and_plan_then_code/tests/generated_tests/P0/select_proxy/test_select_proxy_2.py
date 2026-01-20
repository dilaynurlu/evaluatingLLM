
import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_match():
    url = "http://example.com"
    proxies = {"http": "http://proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
