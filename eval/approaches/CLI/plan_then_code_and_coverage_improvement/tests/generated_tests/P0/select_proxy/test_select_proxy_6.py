from requests.utils import select_proxy

def test_select_proxy_6():
    # Test proxy with 'all' fallback
    url = "ftp://example.com"
    proxies = {"http": "http://p1", "all": "http://p2"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://p2"
