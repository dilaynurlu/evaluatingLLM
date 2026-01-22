from requests.utils import select_proxy

def test_select_proxy_8():
    # Check "all" match (lowest priority)
    proxies = {"all": "http://proxy.com", "http": "http://other.com"}
    url = "ftp://example.com/file"
    assert select_proxy(url, proxies) == "http://proxy.com"
