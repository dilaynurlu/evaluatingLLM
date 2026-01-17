from requests.utils import select_proxy

def test_select_proxy_scheme_match_https():
    # Scenario: Proxy defined for the scheme 'https'.
    # Critique addressed: HTTPS Scheme Support.
    # Ensures the logic works correctly for secure schemes.
    url = "https://example.com/api"
    proxies = {"https": "http://proxy.secure.com"}
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.secure.com"