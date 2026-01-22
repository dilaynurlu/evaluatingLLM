from requests.utils import select_proxy

def test_select_proxy_with_none_proxies():
    """Test that select_proxy returns None when proxies argument is None."""
    url = "http://example.com"
    # When proxies is None, it defaults to empty dict inside the function and returns None
    assert select_proxy(url, None) is None