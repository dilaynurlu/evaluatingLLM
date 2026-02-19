import pytest
from requests.utils import select_proxy

def test_select_proxy_all_match():
    proxies = {
        "all": "http://all.proxy"
    }
    url = "http://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://all.proxy"
