import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_exact_host():
    """
    Test that select_proxy prefers 'scheme://hostname' key over all other keys.
    This corresponds to the highest priority match in the proxy selection logic.
    """
    url = "http://example.com/some/path"
    proxies = {
        "http://example.com": "http://specific-host-proxy",
        "http": "http://scheme-proxy",
        "all://example.com": "http://all-host-proxy",
        "all": "http://global-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://specific-host-proxy"