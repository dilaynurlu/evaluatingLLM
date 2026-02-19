import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test select_proxy with a URL that has no hostname (e.g., a file URI).
    It should bypass the hostname-based lookup loop and directly check for the scheme.
    """
    url = "file:///etc/hosts"
    proxies = {
        "file": "file-proxy",
        "all": "global-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "file-proxy"