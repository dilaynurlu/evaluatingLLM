from requests.utils import select_proxy

def test_select_proxy_2():
    # Scheme match
    proxies = {"http": "http://proxy.com"}
    url = "http://example.com/foo"
    assert select_proxy(url, proxies) == "http://proxy.com"