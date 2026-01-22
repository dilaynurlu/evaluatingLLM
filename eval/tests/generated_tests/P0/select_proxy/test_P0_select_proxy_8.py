from requests.utils import select_proxy

def test_select_proxy_ipv6_host():
    """
    Test IPv6 URL handling. 
    The function uses urlparse which strips brackets, so it should match 
    unbracketed IPv6 addresses in proxy keys.
    """
    url = "http://[::1]"
    proxies = {
        "http://::1": "http://ipv6_proxy",
        "http": "http://generic_proxy"
    }
    # Expect match on "http://::1"
    assert select_proxy(url, proxies) == "http://ipv6_proxy"