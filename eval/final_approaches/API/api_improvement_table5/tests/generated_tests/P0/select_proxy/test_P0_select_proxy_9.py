from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallback():
    # Scenario: Verify behavior when URL has no hostname and specific scheme is missing.
    # It should fall back to "all".
    url = "mailto:user@example.com"
    proxies = {
        "http": "http-proxy",
        "all": "catch-all-proxy"
    }
    # Parsing 'mailto:...' results in a None hostname
    result = select_proxy(url, proxies)
    assert result == "catch-all-proxy"