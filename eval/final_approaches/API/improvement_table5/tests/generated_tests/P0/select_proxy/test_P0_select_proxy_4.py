from requests.utils import select_proxy

def test_select_proxy_scheme_precedence():
    # Scenario: Verify that a scheme-only key (e.g., "http") takes precedence over 
    # "all://hostname" and "all".
    url = "http://example.com/foo"
    proxies = {
        # "http://example.com" is missing
        "http": "http://scheme-proxy",
        "all://example.com": "http://all-host-proxy",
        "all": "http://generic-proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "http://scheme-proxy"