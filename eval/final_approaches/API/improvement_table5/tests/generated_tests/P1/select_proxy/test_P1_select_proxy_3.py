import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_all_host():
    """
    Test that select_proxy prefers 'all://hostname' over the generic 'all' key.
    This validates the third priority level in the proxy selection logic.
    """
    url = "ftp://example.com/file"
    proxies = {
        "all://example.com": "http://all-host-proxy",
        "all": "http://global-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://all-host-proxy"