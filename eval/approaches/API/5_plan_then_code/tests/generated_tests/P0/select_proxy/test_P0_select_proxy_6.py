import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_scheme_over_all():
    """
    Test that a matching scheme key takes precedence over the 'all' key.
    """
    url = "https://secure.example.com"
    proxies = {
        "https": "http://secure-proxy.com",
        "all": "http://fallback-proxy.com"
    }
    
    # 'https' (priority 2) should be selected over 'all' (priority 4)
    # assuming 'https://secure.example.com' (priority 1) is missing
    result = select_proxy(url, proxies)
    assert result == "http://secure-proxy.com"