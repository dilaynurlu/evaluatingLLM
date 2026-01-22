from requests.utils import select_proxy

def test_select_proxy_6():
    # URL with no hostname (file scheme)
    url = "file:///path/to/file"
    proxies = {"file": "http://proxy.com"}
    assert select_proxy(url, proxies) == "http://proxy.com"