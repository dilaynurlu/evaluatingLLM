from requests.utils import select_proxy

def test_select_proxy_all_host_priority():
    """
    Test that 'all://host' key has the third priority when scheme-specific keys are missing.
    """
    url = "http://example.com"
    proxies = {
        "all://example.com": "http://proxy_all_host",
        "all": "http://proxy_all",
    }
    # Should pick the third priority: all://hostname
    assert select_proxy(url, proxies) == "http://proxy_all_host"