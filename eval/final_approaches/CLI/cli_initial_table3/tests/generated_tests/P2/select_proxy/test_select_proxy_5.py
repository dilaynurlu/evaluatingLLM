from requests.utils import select_proxy

def test_select_proxy_empty():
    """
    Test selecting proxy with empty proxies.
    """
    url = "http://example.com/foo"
    
    assert select_proxy(url, {}) is None
    assert select_proxy(url, None) is None
