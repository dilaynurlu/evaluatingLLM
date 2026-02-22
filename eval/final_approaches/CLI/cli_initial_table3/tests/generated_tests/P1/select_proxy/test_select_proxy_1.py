from requests.utils import select_proxy

def test_select_proxy_scheme():
    url = "http://example.com"
    proxies = {"http": "http://proxy.com:8080"}
    
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.com:8080"
    
    # HTTPS
    url2 = "https://example.com"
    proxies2 = {"https": "http://secure.proxy.com:8443"}
    
    proxy2 = select_proxy(url2, proxies2)
    assert proxy2 == "http://secure.proxy.com:8443"
