from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    # If URL is just scheme or something weird
    url = "http:///foo" # No hostname
    proxies = {"http": "http-proxy", "all": "all-proxy"}
    
    # Should use 'http'
    assert select_proxy(url, proxies) == "http-proxy"
    
    del proxies["http"]
    assert select_proxy(url, proxies) == "all-proxy"
