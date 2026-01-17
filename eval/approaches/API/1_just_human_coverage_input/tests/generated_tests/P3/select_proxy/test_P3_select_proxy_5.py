from requests.utils import select_proxy

def test_select_proxy_scheme_precedence_mixed_case():
    # Scenario: Both 'http' and 'all://example.com' are present.
    # Critique addressed: Case Sensitivity & Robustness.
    # Using uppercase scheme in URL to ensure precedence logic handles normalization.
    url = "HTTP://example.com/api"
    
    # Precedence:
    # 1. scheme://hostname (http://example.com) - Not present
    # 2. scheme (http) - Present
    # 3. all://hostname (all://example.com) - Present
    # 'http' should win.
    proxies = {
        "http": "http://proxy.scheme.com",
        "all://example.com": "http://proxy.all-host.com"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.scheme.com"