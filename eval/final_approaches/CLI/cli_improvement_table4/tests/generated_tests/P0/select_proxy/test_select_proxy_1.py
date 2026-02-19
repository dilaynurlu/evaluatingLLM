from requests.utils import select_proxy

def test_select_proxy_1():
    url = "http://example.com"
    proxies = {"http": "http://proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
