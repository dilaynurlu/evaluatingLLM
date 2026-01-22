from requests.utils import select_proxy

def test_select_proxy_scheme_host():
    proxies = {"http://example.com": "http://special-proxy.com"}
    url = "http://example.com/foo"
    assert select_proxy(url, proxies) == "http://special-proxy.com"
