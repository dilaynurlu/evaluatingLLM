from requests.utils import select_proxy

def test_select_proxy_host_match():
    """
    Test selecting proxy by scheme://host.
    """
    url = "http://special.example.com/foo"
    proxies = {
        "http": "http://general.proxy",
        "http://special.example.com": "http://special.proxy"
    }
    
    proxy = select_proxy(url, proxies)
    assert proxy == "http://special.proxy"
