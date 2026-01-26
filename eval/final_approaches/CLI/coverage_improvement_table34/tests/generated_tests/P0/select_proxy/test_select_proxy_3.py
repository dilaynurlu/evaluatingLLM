from requests.utils import select_proxy

def test_select_proxy_3():
    url = "ftp://example.com"
    proxies = {"all": "http://all.proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://all.proxy.com"
