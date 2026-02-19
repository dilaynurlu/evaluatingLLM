from requests.utils import select_proxy

def test_select_proxy_scheme():
    proxies = {"http": "http://proxy.com"}
    url = "http://example.com"
    assert select_proxy(url, proxies) == "http://proxy.com"
