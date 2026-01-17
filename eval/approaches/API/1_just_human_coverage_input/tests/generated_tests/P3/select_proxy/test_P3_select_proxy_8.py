from requests.utils import select_proxy

def test_select_proxy_long_url_fallback():
    # Scenario: Very long URL with unknown scheme/no hostname.
    # Critique addressed: Input Validation / DoS (Long URLs).
    # Ensures function handles large inputs without crashing and falls back correctly.
    long_data = "a" * 2000
    url = f"custom:{long_data}"
    proxies = {
        "all": "http://proxy.fallback.com"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://proxy.fallback.com"