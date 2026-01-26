from requests.utils import select_proxy

def test_select_proxy_all_fallback():
    # Scenario: Verify that "all" is selected when no specific scheme or host matches exist.
    url = "https://example.org/bar"
    proxies = {
        "http": "http://unused-proxy",
        "all": "socks5://fallback-proxy"
    }
    result = select_proxy(url, proxies)
    assert result == "socks5://fallback-proxy"