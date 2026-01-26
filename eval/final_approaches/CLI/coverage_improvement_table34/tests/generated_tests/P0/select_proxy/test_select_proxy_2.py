from requests.utils import select_proxy

def test_select_proxy_2():
    url = "http://example.com"
    proxies = {"http://example.com": "http://specific.proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://specific.proxy.com"
