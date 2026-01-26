from requests.utils import select_proxy

def test_select_proxy_scheme_priority():
    """
    Test that 'scheme' key has the second priority when the specific host key is missing.
    """
    url = "http://example.com"
    proxies = {
        "http": "http://proxy_scheme",
        "all://example.com": "http://proxy_all_host",
        "all": "http://proxy_all",
    }
    # Should pick the second priority: scheme
    assert select_proxy(url, proxies) == "http://proxy_scheme"