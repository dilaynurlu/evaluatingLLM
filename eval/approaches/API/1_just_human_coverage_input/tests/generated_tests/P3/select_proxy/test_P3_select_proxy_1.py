from requests.utils import select_proxy

def test_select_proxy_exact_match_mixed_case():
    # Scenario: Proxy defined exactly for this scheme and host.
    # Critique addressed: Case Sensitivity.
    # The URL contains mixed case scheme and host. The proxy key is lowercase.
    # select_proxy should normalize the URL components to match the key.
    url = "HtTp://ExAmPlE.cOm/ApI"
    proxies = {"http://example.com": "http://proxy.example.com"}
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.example.com"