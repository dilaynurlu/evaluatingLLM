from requests.utils import select_proxy

def test_select_proxy_priority_scheme_vs_all_host():
    url = "http://example.com"
    proxies = {
        "http": "http://proxy.scheme.com",
        "all://example.com": "http://proxy.all_host.com"
    }
    
    # Priority check: Scheme match (http) should generally be preferred over generic 'all' host match
    result = select_proxy(url, proxies)
    assert result == "http://proxy.scheme.com", \
        f"Expected scheme match to have priority over 'all://host'. Got: {result}"