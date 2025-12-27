import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_only_match():
    """
    Test selecting a proxy defined for the scheme only (e.g., 'http').
    This should be selected if the specific 'scheme://hostname' is not present.
    """
    url = "http://www.example.com/resource"
    proxies = {
        "http": "http://scheme-proxy.com:8080",
        "all": "http://fallback-proxy.com:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://scheme-proxy.com:8080"