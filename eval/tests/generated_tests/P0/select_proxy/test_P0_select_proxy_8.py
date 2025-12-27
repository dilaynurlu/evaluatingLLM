import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test selecting a proxy when the URL has no hostname (e.g. mailto: links).
    In this case, the function should look up proxies by scheme directly.
    """
    url = "mailto:user@example.com"
    # mailto URLs typically parse with hostname=None
    proxies = {
        "mailto": "http://mail-proxy.com",
        "all": "http://all-proxy.com"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://mail-proxy.com"