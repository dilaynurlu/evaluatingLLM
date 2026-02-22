from requests.utils import select_proxy

def test_select_proxy_host_specific():
    url = "http://example.com"
    proxies = {
        "http://example.com": "http://specific.proxy.com",
        "http": "http://generic.proxy.com"
    }
    
    # Should select specific one first
    proxy = select_proxy(url, proxies)
    assert proxy == "http://specific.proxy.com"
