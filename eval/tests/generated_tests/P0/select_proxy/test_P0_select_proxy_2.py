from requests.utils import select_proxy

def test_select_proxy_scheme_host_priority():
    """
    Test that 'scheme://host' key has the highest priority when selecting a proxy.
    """
    url = "http://example.com"
    proxies = {
        "http://example.com": "http://proxy_exact",
        "http": "http://proxy_scheme",
        "all://example.com": "http://proxy_all_host",
        "all": "http://proxy_all",
    }
    # Should pick the first priority: scheme://hostname
    assert select_proxy(url, proxies) == "http://proxy_exact"