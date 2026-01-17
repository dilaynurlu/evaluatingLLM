import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_all_fallback():
    """
    Test select_proxy behavior for URLs without a hostname when scheme is missing.
    Should fall back to 'all'.
    """
    url = "file:///etc/hosts"
    proxies = {
        "http": "http_proxy",
        "all": "global_proxy"
    }
    
    assert select_proxy(url, proxies) == "global_proxy"