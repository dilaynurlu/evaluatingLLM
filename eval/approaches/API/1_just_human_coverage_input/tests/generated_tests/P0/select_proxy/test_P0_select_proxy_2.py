import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_match():
    """
    Test that select_proxy selects a proxy defined for the URL's scheme
    when no exact hostname match is available.
    """
    url = "https://example.org/resource"
    proxies = {
        "https": "http://secure-proxy.local:3128",
        "all": "http://fallback-proxy.local:3128"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://secure-proxy.local:3128"