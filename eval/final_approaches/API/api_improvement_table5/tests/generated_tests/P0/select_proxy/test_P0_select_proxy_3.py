from requests.utils import select_proxy

def test_select_proxy_exact_match():
    # Scenario: Verify precedence where a specific "scheme://hostname" key exists.
    # It should take priority over "scheme", "all://hostname", and "all".
    url = "http://example.com/foo"
    proxies = {
        "http://example.com": "http://specific-host-proxy",
        "http": "http://scheme-proxy",
        "all://example.com": "http://all-host-proxy",
        "all": "http://generic-proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://specific-host-proxy"