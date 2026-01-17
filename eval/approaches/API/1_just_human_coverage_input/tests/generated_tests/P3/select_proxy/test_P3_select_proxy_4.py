from requests.utils import select_proxy

def test_select_proxy_all_match_cross_protocol():
    # Scenario: Proxy defined for 'all' as a catch-all.
    # Critique addressed: Cross-Protocol Mapping.
    # Verifies mapping an HTTPS URL to an HTTP proxy (tunneling).
    url = "https://example.com/api"
    proxies = {"all": "http://proxy.catchall.com"}
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.catchall.com"