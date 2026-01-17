from requests.utils import select_proxy

def test_select_proxy_exact_precedence_over_scheme_https():
    # Scenario: Both 'https://example.com' and 'https' are present.
    # Critique addressed: HTTPS Support & Precedence.
    url = "https://example.com/api"
    proxies = {
        "https://example.com": "http://proxy.exact.com",
        "https": "http://proxy.scheme.com"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.exact.com"