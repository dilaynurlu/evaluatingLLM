from requests.utils import select_proxy

def test_select_proxy_scheme_host():
    url = "http://example.com"
    proxies = {"http://example.com": "http://specific.com"}
    assert select_proxy(url, proxies) == "http://specific.com"
