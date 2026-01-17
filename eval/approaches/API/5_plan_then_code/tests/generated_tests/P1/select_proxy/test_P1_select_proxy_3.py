from requests.utils import select_proxy

def test_select_proxy_scheme_only_match():
    """
    Test that select_proxy falls back to 'scheme' match if 'scheme://hostname' is not found.
    """
    proxies = {
        "http": "http://proxy.general.com",
        "all": "http://proxy.fallback.com"
    }
    url = "http://example.com/some/path"
    
    # Expect the scheme match
    assert select_proxy(url, proxies) == "http://proxy.general.com"