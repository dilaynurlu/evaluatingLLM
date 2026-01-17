import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence():
    proxies = {
        "http://example.com": "http://specific.proxy",
        "http": "http://generic.proxy",
        "all": "http://all.proxy"
    }
    url = "http://example.com"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://specific.proxy"
    
    url2 = "http://other.com"
    proxy2 = select_proxy(url2, proxies)
    assert proxy2 == "http://generic.proxy"
