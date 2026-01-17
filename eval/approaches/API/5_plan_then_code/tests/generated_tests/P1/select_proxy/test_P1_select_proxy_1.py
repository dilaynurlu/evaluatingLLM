from requests.utils import select_proxy

def test_select_proxy_returns_none_when_proxies_is_none():
    """
    Test that select_proxy returns None when the proxies argument is None.
    It should handle None gracefully by treating it as an empty dictionary.
    """
    url = "http://example.com"
    # Passing None for proxies should not raise an exception and should return None
    assert select_proxy(url, None) is None