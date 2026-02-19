import pytest
from requests.utils import select_proxy

def test_select_proxy_matches_scheme_when_hostname_is_none():
    """
    Test that select_proxy correctly matches the scheme in the proxies dictionary
    when the URL does not contain a hostname (e.g., mailto: or file: without netloc).
    """
    # A generic URI scheme that typically results in hostname=None
    url = "mailto:user@example.com"
    proxies = {
        "mailto": "http://mail.proxy.server:3128"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://mail.proxy.server:3128"