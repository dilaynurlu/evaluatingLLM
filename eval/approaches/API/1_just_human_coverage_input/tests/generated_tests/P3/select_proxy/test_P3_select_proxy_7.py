from requests.utils import select_proxy

def test_select_proxy_no_hostname_mixed_case_scheme():
    # Scenario: URL has no hostname, scheme mixed case.
    # Critique addressed: Fuzzy Scheme Matching / Case Sensitivity.
    url = "MaiLTo:user@example.com"
    proxies = {"mailto": "http://proxy.mail.com"}
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.mail.com"