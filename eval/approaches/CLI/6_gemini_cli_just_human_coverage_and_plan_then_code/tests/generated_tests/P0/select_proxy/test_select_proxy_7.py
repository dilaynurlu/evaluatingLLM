
import pytest
from requests.utils import select_proxy

def test_select_proxy_all_host_match():
    url = "http://example.com"
    proxies = {"all://example.com": "http://proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
