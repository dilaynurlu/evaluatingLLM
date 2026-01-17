from requests.utils import select_proxy

def test_select_proxy_priority():
    # Priority: scheme://host > scheme > all://host > all
    url = "http://example.com"
    proxies = {
        "http://example.com": "1",
        "http": "2",
        "all://example.com": "3",
        "all": "4"
    }
    assert select_proxy(url, proxies) == "1"
    
    del proxies["http://example.com"]
    assert select_proxy(url, proxies) == "2"
    
    del proxies["http"]
    assert select_proxy(url, proxies) == "3"
    
    del proxies["all://example.com"]
    assert select_proxy(url, proxies) == "4"
