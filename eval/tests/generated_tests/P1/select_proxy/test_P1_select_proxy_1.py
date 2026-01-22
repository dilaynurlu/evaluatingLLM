from requests.utils import select_proxy

def test_select_proxy_precedence_scheme_host_over_scheme():
    """
    Test that a proxy defined specifically for 'scheme://hostname' takes precedence
    over a proxy defined generally for 'scheme'.
    """
    url = "http://example.com/foo"
    proxies = {
        "http://example.com": "http://specific-proxy.com",
        "http": "http://general-scheme-proxy.com",
        "all://example.com": "http://all-host-proxy.com",
        "all": "http://all-proxy.com",
    }
    
    # Expected behavior: The first key in the search list is 'scheme://hostname'.
    # For 'http://example.com', the key is 'http://example.com'.
    result = select_proxy(url, proxies)
    assert result == "http://specific-proxy.com"