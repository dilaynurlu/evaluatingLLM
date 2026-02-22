from requests.utils import select_proxy

def test_select_proxy_no_match():
    """
    Test selecting proxy with no match.
    """
    url = "ftp://example.com/foo"
    proxies = {
        "http": "http://proxy.example.com"
    }
    
    proxy = select_proxy(url, proxies)
    assert proxy is None
