from requests.utils import select_proxy

def test_select_proxy_all():
    url = "http://example.com"
    proxies = {"all": "http://proxy.com"}
    assert select_proxy(url, proxies) == "http://proxy.com"
