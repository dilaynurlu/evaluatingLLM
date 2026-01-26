from requests.utils import select_proxy

def test_select_proxy_5():
    # Test proxy with all://hostname
    url = "http://example.com"
    proxies = {"all://example.com": "http://proxy.com"}
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com"
