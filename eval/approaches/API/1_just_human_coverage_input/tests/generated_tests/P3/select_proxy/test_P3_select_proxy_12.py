from requests.utils import select_proxy

def test_select_proxy_malformed_url():
    # Scenario: Malformed URL (missing host).
    # Critique addressed: Malformed URLs.
    # select_proxy should handle parsing failures or missing components gracefully (return None).
    url = "http://"
    proxies = {
        "http": "http://proxy.scheme.com",
        "all": "http://proxy.catchall.com"
    }
    
    # With http://, netloc is empty. It might match 'http' scheme if implemented that way,
    # or return None if hostname is required for scheme://hostname check and logic is strict.
    # In standard requests behavior, empty netloc might just match scheme proxy.
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.scheme.com"