from requests.utils import select_proxy

def test_select_proxy_priority_scheme_over_all_host():
    """
    Test the precedence order: verifies that a generic 'scheme' match 
    takes precedence over an 'all://hostname' match.
    
    The priority list is:
    1. scheme://hostname
    2. scheme
    3. all://hostname
    4. all
    """
    proxies = {
        "http": "http://proxy.scheme",
        "all://example.com": "http://proxy.all_host"
    }
    url = "http://example.com"
    
    # 'http' (2) should beat 'all://example.com' (3)
    assert select_proxy(url, proxies) == "http://proxy.scheme"