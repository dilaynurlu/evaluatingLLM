from requests.utils import select_proxy

def test_select_proxy_no_match():
    proxies = {"http": "p1"}
    url = "ftp://example.com"
    assert select_proxy(url, proxies) is None
