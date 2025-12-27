import pytest
from requests.utils import select_proxy

def test_select_proxy_fallback_all():
    """
    Test that select_proxy falls back to the generic 'all' key when
    no specific host or scheme matches are found in the proxies dictionary.
    """
    url = "http://example.com/resource"
    proxies = {
        "https": "http://secure-proxy.com",  # Different scheme
        "ftp://example.com": "http://ftp-proxy.com",  # Different scheme specific
        "all": "http://catch-all-proxy.com",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://catch-all-proxy.com"