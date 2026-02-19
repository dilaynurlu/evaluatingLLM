from requests.utils import select_proxy

def test_select_proxy_no_hostname_match_all():
    """
    Test proxy selection for a URL with no hostname when scheme proxy is missing.
    It should fallback to 'all'.
    """
    url = "file:///etc/hosts"
    proxies = {
        "http": "http://http-proxy.com",
        "all": "http://generic-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://generic-proxy.com"