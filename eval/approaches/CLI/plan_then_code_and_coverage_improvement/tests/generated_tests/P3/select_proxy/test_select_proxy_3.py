from requests.utils import select_proxy

def test_select_proxy_3():
    # All match
    proxies = {"all": "http://proxy.com"}
    url = "ftp://example.com/foo"
    assert select_proxy(url, proxies) == "http://proxy.com"
