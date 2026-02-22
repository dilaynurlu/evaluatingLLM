from requests.utils import select_proxy

def test_select_proxy_3():
    url = "ftp://example.com"
    proxies = {"all": "http://fallback.com"}
    assert select_proxy(url, proxies) == "http://fallback.com"
