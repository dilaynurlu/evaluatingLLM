from requests.utils import select_proxy

def test_select_proxy_4():
    url = "http://example.com"
    proxies = {"https": "http://secure.proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy is None
