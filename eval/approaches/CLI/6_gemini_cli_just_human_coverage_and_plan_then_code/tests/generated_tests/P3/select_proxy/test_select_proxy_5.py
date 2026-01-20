from requests.utils import select_proxy

def test_select_proxy_none_found():
    url = "http://example.com"
    proxies = {"https": "secure.com"}
    assert select_proxy(url, proxies) is None
