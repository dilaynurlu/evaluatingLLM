import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    proxies = {"file": "http://file.proxy"}
    url = "file:///etc/hosts"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://file.proxy"
