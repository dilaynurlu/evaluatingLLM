import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_match():
    proxies = {
        "http": "http://generic.proxy"
    }
    url = "http://example.com/foo"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://generic.proxy"
