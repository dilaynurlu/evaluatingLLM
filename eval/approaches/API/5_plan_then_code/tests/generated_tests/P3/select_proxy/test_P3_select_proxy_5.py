import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test select_proxy behavior for URLs without a hostname (e.g., file://).
    Should match based on scheme.
    """
    # file:///path indicates no authority/hostname
    url = "file:///etc/hosts"
    proxies = {
        "file": "file_proxy",
        "http": "http_proxy"
    }
    
    assert select_proxy(url, proxies) == "file_proxy"