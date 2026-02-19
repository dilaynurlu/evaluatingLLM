import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallback_all():
    """
    Test select_proxy with a URL that has no hostname (e.g., a file URI),
    where the scheme is not in proxies. It should fallback to the 'all' key.
    """
    url = "file:///etc/hosts"
    proxies = {
        "http": "http-proxy",
        "all": "global-proxy",
    }
    
    result = select_proxy(url, proxies)
    assert result == "global-proxy"