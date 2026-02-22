from requests.utils import select_proxy

def test_select_proxy_all():
    url = "ftp://example.com"
    proxies = {"all": "socks5://all.proxy.com"}
    
    proxy = select_proxy(url, proxies)
    assert proxy == "socks5://all.proxy.com"
    
    # 'all' specific host
    proxies2 = {
        "all://example.com": "socks5://specific.proxy.com",
        "all": "socks5://generic.proxy.com"
    }
    proxy2 = select_proxy(url, proxies2)
    assert proxy2 == "socks5://specific.proxy.com"
