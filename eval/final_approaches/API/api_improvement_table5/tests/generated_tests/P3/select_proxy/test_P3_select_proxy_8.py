from requests.utils import select_proxy

def test_select_proxy_none_args():
    """
    Test select_proxy handles a None proxies argument gracefully by treating it
    as an empty dictionary and returning None.
    """
    url = "http://example.com"
    
    # Passing None for proxies should result in None return (no proxy selected)
    assert select_proxy(url, None) is None