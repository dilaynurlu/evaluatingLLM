import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_priority_over_all_host():
    """
    Test that a proxy defined for a scheme takes precedence over
    an 'all://hostname' proxy.
    """
    url = "https://example.com/secure"
    proxies = {
        "https": "http://scheme-proxy.local:1080",
        "all://example.com": "http://host-all-proxy.local:8888",
        "all": "http://fallback.local:80"
    }
    
    # Expected: 'https' comes before 'all://example.com' in the lookup order
    result = select_proxy(url, proxies)
    assert result == "http://scheme-proxy.local:1080"