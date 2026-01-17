import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test proxy selection for a URL without a hostname (e.g. file:// scheme).
    It should try to match the scheme first.
    """
    # A file URL with three slashes implies an empty authority (hostname is None/empty)
    url = "file:///etc/passwd" 
    proxies = {
        "file": "file-proxy-handler",
        "all": "fallback-proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "file-proxy-handler"