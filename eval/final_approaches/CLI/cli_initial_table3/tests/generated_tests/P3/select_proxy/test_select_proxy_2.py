import pytest
from requests.utils import select_proxy

def test_select_proxy_2():
    proxies = {"all": "http://proxy.com"}
    url = "https://example.com"
    assert select_proxy(url, proxies) == "http://proxy.com"
