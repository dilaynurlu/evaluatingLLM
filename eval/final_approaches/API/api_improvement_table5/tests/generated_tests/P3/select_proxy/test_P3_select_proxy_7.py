from requests.utils import select_proxy

def test_select_proxy_ipv6():
    """
    Test select_proxy correctly constructs keys for IPv6 hostnames.
    The constructed key should use the unbracketed IPv6 address.
    
    Refinement:
    - Uses https scheme to verify behavior works across different schemes.
    """
    url = "https://[2001:db8::1]:8443/path"
    
    # Note: select_proxy uses urlparse which strips brackets from hostname.
    # The proxy key expected is scheme://unbracketed_host
    proxies = {
        "https://2001:db8::1": "http://ipv6-proxy"
    }
    
    assert select_proxy(url, proxies) == "http://ipv6-proxy"