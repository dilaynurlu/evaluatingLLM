import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname():
    """
    Test select_proxy behavior for URLs without a hostname (e.g., file:// scheme).
    
    When hostname is None, the function checks proxies.get(scheme), 
    then proxies.get("all").
    """
    url = "file:///etc/hosts"
    proxies = {
        "file": "http://file-inspector-proxy",
        "http": "http://web-proxy",
        "all": "http://global-proxy"
    }
    
    # Should match the scheme 'file' directly
    expected_proxy = "http://file-inspector-proxy"
    assert select_proxy(url, proxies) == expected_proxy