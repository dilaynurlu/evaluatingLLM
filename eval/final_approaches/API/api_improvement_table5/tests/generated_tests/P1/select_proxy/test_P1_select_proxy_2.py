import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_scheme():
    """
    Test that select_proxy prefers the 'scheme' key over 'all://hostname' and 'all'.
    This validates the second priority level in the proxy selection logic.
    """
    url = "http://example.com/some/path"
    proxies = {
        "http": "http://scheme-proxy",
        "all://example.com": "http://all-host-proxy",
        "all": "http://global-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://scheme-proxy"