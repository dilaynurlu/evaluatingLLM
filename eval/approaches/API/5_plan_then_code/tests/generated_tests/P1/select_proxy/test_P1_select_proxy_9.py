from requests.utils import select_proxy

def test_select_proxy_ipv6_hostname():
    """
    Test proxy selection for an IPv6 URL. 
    The function constructs the key using the hostname without brackets (from urlparse).
    """
    # Note: requests.utils.select_proxy uses urlparse, which strips brackets from IPv6 hostnames.
    # Therefore, the proxy key must be "scheme://unbracketed_ipv6".
    proxies = {
        "http://::1": "http://ipv6.local.proxy"
    }
    # URL with bracketed IPv6 and port
    url = "http://[::1]:8080/foo"
    
    assert select_proxy(url, proxies) == "http://ipv6.local.proxy"