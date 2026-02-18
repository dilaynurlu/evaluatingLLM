from requests.utils import select_proxy

def test_select_proxy_all_host():
    proxies = {"all://example.com": "http://special.com"}
    url = "ftp://example.com"
    assert select_proxy(url, proxies) == "http://special.com"
