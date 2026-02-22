from requests.utils import select_proxy

def test_select_proxy_all():
    """
    Test selecting proxy by 'all'.
    """
    url = "ftp://example.com/foo"
    proxies = {
        "all": "socks5://proxy.example.com"
    }
    
    proxy = select_proxy(url, proxies)
    assert proxy == "socks5://proxy.example.com"
