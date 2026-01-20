
import pytest
from requests.utils import select_proxy

def test_select_proxy_none_proxies():
    url = "http://example.com"
    proxy = select_proxy(url, None)
    assert proxy is None
