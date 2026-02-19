import pytest
from requests.utils import select_proxy

def test_select_proxy_fallback_to_all():
    """
    Test that select_proxy falls back to the 'all' key when no specific keys 
    (scheme-host, scheme, or all-host) are present in the proxies dictionary.
    """
    url = "https://example.com/secure"
    proxies = {
        "all": "http://global-proxy",
        "http": "http://unused-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://global-proxy"