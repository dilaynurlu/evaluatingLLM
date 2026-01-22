from requests.utils import select_proxy

def test_select_proxy_precedence_all_host_over_all():
    """
    Test that a proxy defined for 'all://hostname' takes precedence over 'all'.
    """
    url = "http://example.com/foo"
    proxies = {
        "all://example.com": "http://all-host-proxy.com",
        "all": "http://all-proxy.com",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://all-host-proxy.com"