
import pytest
from requests.utils import select_proxy

def test_select_proxy_hostname_none():
    url = "file:///path/to/file"
    proxies = {"file": "http://proxy.com"}
    # If hostname is None, it tries scheme or all
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
