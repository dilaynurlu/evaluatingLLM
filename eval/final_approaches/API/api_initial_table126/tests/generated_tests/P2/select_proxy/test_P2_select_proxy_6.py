import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_file_scheme():
    """
    Test that URLs without a hostname (like file://) correctly match
    proxies defined for their scheme.
    """
    url = "file:///etc/passwd"
    proxies = {
        "file": "http://file-proxy.local",
        "all": "http://all-proxy.local"
    }
    
    # Logic for no hostname:
    # return proxies.get(scheme, proxies.get("all"))
    # Should find 'file'
    expected = "http://file-proxy.local"
    assert select_proxy(url, proxies) == expected