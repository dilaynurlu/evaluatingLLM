from requests.utils import select_proxy

def test_select_proxy_all_host_match_credentials():
    # Scenario: Proxy defined for 'all' schemes on this host.
    # Critique addressed: Credential Handling.
    # Ensures that the returned proxy string retains authentication information.
    url = "http://example.com/api"
    proxies = {"all://example.com": "http://user:pass@proxy.auth.com"}
    
    result = select_proxy(url, proxies)
    
    assert result == "http://user:pass@proxy.auth.com"