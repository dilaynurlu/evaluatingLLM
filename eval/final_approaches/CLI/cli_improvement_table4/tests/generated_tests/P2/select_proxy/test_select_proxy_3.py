from requests.utils import select_proxy

def test_select_proxy_all():
    proxies = {"all": "http://fallback.com"}
    url = "ftp://example.com"
    assert select_proxy(url, proxies) == "http://fallback.com"
