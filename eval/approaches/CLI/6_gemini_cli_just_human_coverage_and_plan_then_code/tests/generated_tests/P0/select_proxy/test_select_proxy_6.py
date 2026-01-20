
import pytest
from requests.utils import select_proxy

def test_select_proxy_specific_host_precedence():
    url = "http://example.com"
    proxies = {
        "http": "http://general-proxy.com",
        "http://example.com": "http://specific-proxy.com"
    }
    proxy = select_proxy(url, proxies)
    assert proxy == "http://specific-proxy.com"
