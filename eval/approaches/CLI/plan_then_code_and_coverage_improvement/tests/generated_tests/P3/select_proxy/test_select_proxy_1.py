from requests.utils import select_proxy

def test_select_proxy_1():
    # Exact scheme://host match
    proxies = {"http://example.com": "http://proxy.com"}
    url = "http://example.com/foo"
    assert select_proxy(url, proxies) == "http://proxy.com"