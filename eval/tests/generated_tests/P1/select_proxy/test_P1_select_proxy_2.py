from requests.utils import select_proxy

def test_select_proxy_precedence_scheme_over_all_host():
    """
    Test that a proxy defined for 'scheme' takes precedence over 'all://hostname'.
    
    Note: verify the internal priority list:
    1. scheme://hostname
    2. scheme
    3. all://hostname
    4. all
    """
    url = "http://example.com/foo"
    proxies = {
        "http": "http://scheme-proxy.com",
        "all://example.com": "http://all-host-proxy.com",
        "all": "http://all-proxy.com",
    }
    
    # Even though 'all://example.com' is host-specific, the implementation checks 'scheme' first.
    result = select_proxy(url, proxies)
    assert result == "http://scheme-proxy.com"