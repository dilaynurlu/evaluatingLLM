import pytest
from requests.utils import select_proxy

def test_select_proxy_explicit_disable():
    """
    Refined test for 'scheme match' covering 'Explicit Disable'.
    Verifies that mapping a specific host key to None effectively disables 
    proxying for that host, preventing fallback to broader scheme or 'all' proxies.
    """
    url = "http://example.com/some/path"
    proxies = {
        # Explicitly disable proxy for this host
        "http://example.com": None,
        # A general scheme proxy exists
        "http": "http://proxy.general-scheme:8080",
        # A global fallback exists
        "all": "http://proxy.fallback:8080",
    }
    
    # Should stop at the specific match and return None, not fall back
    result = select_proxy(url, proxies)
    assert result is None