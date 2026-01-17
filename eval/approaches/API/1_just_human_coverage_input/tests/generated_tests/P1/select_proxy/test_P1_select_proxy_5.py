import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_scheme_match():
    """
    Test behavior when URL has no hostname (e.g. file scheme).
    Should try to match the scheme.
    """
    url = "file:///etc/passwd"
    proxies = {
        "file": "http://file-inspector.local:8000",
        "all": "http://catch-all.local:80"
    }
    
    # urlparse('file:///...') results in hostname=None.
    # Logic path: return proxies.get(scheme, ...)
    result = select_proxy(url, proxies)
    assert result == "http://file-inspector.local:8000"