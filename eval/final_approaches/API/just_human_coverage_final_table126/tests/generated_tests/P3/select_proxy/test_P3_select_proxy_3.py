from requests.utils import select_proxy

def test_select_proxy_scheme_match():
    url = "http://www.google.com/search"
    proxies = {
        "http": "http://proxy.generic.com",
        "all": "http://proxy.fallback.com"
    }
    
    # Verify standard scheme match
    result = select_proxy(url, proxies)
    assert result == "http://proxy.generic.com", \
        f"Expected generic scheme match 'http'. Got: {result}"
        
    # Verify behavior with empty values (critique point: Empty Proxy Values)
    # This ensures that an empty string is returned as-is, implying 'no proxy' or explicit empty config
    proxies_empty = {"http": ""}
    assert select_proxy(url, proxies_empty) == "", \
        "Expected empty string to be returned when proxy value is empty string"