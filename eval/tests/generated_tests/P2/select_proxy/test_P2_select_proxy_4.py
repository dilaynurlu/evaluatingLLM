import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_logic():
    """
    Test scenarios where the URL has no hostname (e.g., file://),
    verifying it follows the logic branch for hostname is None.
    
    It should prioritize the scheme specific key over 'all'.
    """
    url = "file:///etc/motd"
    proxies = {
        "file": "http://file-proxy.local",
        "all": "http://fallback-proxy.local",
    }
    
    # For file:/// paths, urlparse returns None (or empty) for hostname,
    # triggering the 'if urlparts.hostname is None' block.
    result = select_proxy(url, proxies)
    
    assert result == "http://file-proxy.local"