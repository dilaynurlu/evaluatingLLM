import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test select_proxy with a URL that has no hostname (e.g., mailto:).
    It should match based on the scheme if available.
    """
    url = "mailto:user@example.com"
    proxies = {
        "mailto": "http://mail-proxy.com",
        "all": "http://fallback-proxy.com",
    }
    
    # mailto URLs typically parse with hostname=None
    result = select_proxy(url, proxies)
    assert result == "http://mail-proxy.com"