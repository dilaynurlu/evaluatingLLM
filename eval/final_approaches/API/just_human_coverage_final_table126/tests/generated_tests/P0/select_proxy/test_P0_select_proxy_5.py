from requests.utils import select_proxy

def test_select_proxy_all_priority():
    """
    Test that 'all' key has the lowest priority and serves as a fallback.
    """
    url = "http://example.com"
    proxies = {
        "all": "http://proxy_all",
    }
    # Should pick the fourth priority: all
    assert select_proxy(url, proxies) == "http://proxy_all"