
import pytest
from requests.utils import select_proxy

def test_select_proxy_all_match():
    url = "ftp://example.com"
    proxies = {"all": "http://proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
