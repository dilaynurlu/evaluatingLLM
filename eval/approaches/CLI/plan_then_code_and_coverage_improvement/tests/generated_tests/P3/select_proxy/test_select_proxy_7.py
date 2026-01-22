from requests.utils import select_proxy

def test_select_proxy_7():
    # Check "all://hostname" match
    proxies = {"all://example.com": "http://proxy.com"}
    url = "ftp://example.com/file"
    assert select_proxy(url, proxies) == "http://proxy.com"
