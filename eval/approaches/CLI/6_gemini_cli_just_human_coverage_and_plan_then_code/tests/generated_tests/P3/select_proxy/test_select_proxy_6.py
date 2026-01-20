from requests.utils import select_proxy

def test_select_proxy_empty_dict():
    url = "http://example.com"
    proxies = {}
    assert select_proxy(url, proxies) is None
