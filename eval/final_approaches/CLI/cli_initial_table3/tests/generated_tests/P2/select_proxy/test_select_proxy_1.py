from requests.utils import select_proxy

def test_select_proxy_exact_scheme():
    """
    Test selecting proxy by scheme.
    """
    url = "http://example.com/foo"
    proxies = {
        "http": "http://proxy.example.com",
        "https": "https://proxy.example.com"
    }
    
    proxy = select_proxy(url, proxies)
    assert proxy == "http://proxy.example.com"
