from requests.utils import select_proxy

def test_select_proxy_scheme():
    url = "http://example.com"
    proxies = {"http": "http://proxy.com"}
    assert select_proxy(url, proxies) == "http://proxy.com"
