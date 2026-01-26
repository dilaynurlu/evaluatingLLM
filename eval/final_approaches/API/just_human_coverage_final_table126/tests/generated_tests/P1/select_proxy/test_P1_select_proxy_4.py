from requests.utils import select_proxy

def test_select_proxy_ipv6_host():
    """
    Test proxy selection for an IPv6 URL.
    The hostname extracted from 'http://[::1]' should be '::1' (without brackets).
    The key generated should be 'http://::1'.
    """
    url = "http://[2001:db8::1]/path"
    proxies = {
        "http://2001:db8::1": "http://ipv6-proxy.com",
        "all": "http://fallback-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://ipv6-proxy.com"