from requests.utils import select_proxy

def test_select_proxy_exact_scheme_host_match():
    """
    Test that select_proxy prioritizes a match for 'scheme://hostname'.
    """
    proxies = {
        "http://example.com": "http://proxy.example.com",
        "http": "http://proxy.general.com"
    }
    url = "http://example.com/some/path"
    
    # Expect the specific scheme://host match
    assert select_proxy(url, proxies) == "http://proxy.example.com"