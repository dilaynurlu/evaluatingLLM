import pytest
from requests.utils import select_proxy

def test_select_proxy_specific_host_precedence():
    # scheme://host should beat scheme
    proxies = {
        "http://example.com": "http://specific-proxy",
        "http": "http://generic-proxy"
    }
    url = "http://example.com"
    proxy = select_proxy(url, proxies)
    assert proxy == "http://specific-proxy"
