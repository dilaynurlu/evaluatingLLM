from requests.utils import select_proxy

def test_select_proxy_none():
    url = "http://www.google.com"
    # Test with None
    assert select_proxy(url, None) is None, "Expected None when proxies argument is None"
    
    # Test with empty dictionary
    assert select_proxy(url, {}) is None, "Expected None when proxies argument is an empty dictionary"