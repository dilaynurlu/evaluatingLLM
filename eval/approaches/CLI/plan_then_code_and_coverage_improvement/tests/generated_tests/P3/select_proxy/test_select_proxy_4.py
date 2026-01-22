from requests.utils import select_proxy

def test_select_proxy_4():
    # No match
    proxies = {"https": "http://secure.com"}
    url = "http://example.com"
    assert select_proxy(url, proxies) is None
