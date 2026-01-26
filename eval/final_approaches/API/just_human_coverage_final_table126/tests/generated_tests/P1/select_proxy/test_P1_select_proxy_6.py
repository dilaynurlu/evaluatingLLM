from requests.utils import select_proxy

def test_select_proxy_no_hostname_match_scheme():
    """
    Test proxy selection for a URL with no hostname (e.g. file://).
    It should match based on the scheme if available.
    """
    url = "file:///etc/hosts"
    proxies = {
        "file": "http://file-proxy.com",
        "all": "http://all-proxy.com"
    }
    
    # For URLs without hostname, it attempts proxies.get(scheme) then proxies.get("all")
    result = select_proxy(url, proxies)
    assert result == "http://file-proxy.com"