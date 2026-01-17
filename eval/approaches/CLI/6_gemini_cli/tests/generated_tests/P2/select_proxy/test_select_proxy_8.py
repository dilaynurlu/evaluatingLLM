import pytest
from requests.utils import select_proxy

def test_select_proxy_url_with_port():
    proxies = {"http": "http://proxy"}
    url = "http://example.com:8080"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy"
