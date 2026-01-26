from requests.utils import select_proxy

def test_select_proxy_7():
    # Test precedence: scheme://host > scheme > all://host > all
    url = "http://example.com"
    proxies = {
        "http://example.com": "p1",
        "http": "p2",
        "all://example.com": "p3",
        "all": "p4"
    }
    assert select_proxy(url, proxies) == "p1"
    
    proxies.pop("http://example.com")
    assert select_proxy(url, proxies) == "p2"
    
    proxies.pop("http")
    assert select_proxy(url, proxies) == "p3"
    
    proxies.pop("all://example.com")
    assert select_proxy(url, proxies) == "p4"
