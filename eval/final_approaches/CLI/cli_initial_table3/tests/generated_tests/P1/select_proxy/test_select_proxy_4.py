from requests.utils import select_proxy

def test_select_proxy_priority():
    url = "http://example.com"
    proxies = {
        "http://example.com": "specific-host-scheme",
        "http": "scheme-generic",
        "all://example.com": "specific-host-all",
        "all": "all-generic"
    }
    
    # 1. scheme://hostname
    assert select_proxy(url, proxies) == "specific-host-scheme"
    
    del proxies["http://example.com"]
    # 2. scheme
    assert select_proxy(url, proxies) == "scheme-generic"
    
    del proxies["http"]
    # 3. all://hostname
    assert select_proxy(url, proxies) == "specific-host-all"
    
    del proxies["all://example.com"]
    # 4. all
    assert select_proxy(url, proxies) == "all-generic"
    
    del proxies["all"]
    # None
    assert select_proxy(url, proxies) is None
