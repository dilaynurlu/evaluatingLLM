from requests.utils import select_proxy

def test_select_proxy_none_proxies():
    """
    Test that select_proxy handles None as the proxies argument gracefully,
    returning None.
    """
    url = "http://example.com"
    result = select_proxy(url, None)
    assert result is None