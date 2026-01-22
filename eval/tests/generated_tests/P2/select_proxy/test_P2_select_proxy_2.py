import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_only_match():
    """
    Test that select_proxy falls back to the scheme-only key
    when a specific scheme://hostname key is not present.
    """
    url = "http://example.org/index.html"
    proxies = {
        "http": "http://proxy-scheme.local:3128",
        "all://example.org": "http://proxy-all-host.local:3128",
        "all": "socks5://proxy-fallback.local:1080"
    }
    
    # Logic: 'http://example.org' (missing) -> 'http' (present)
    # 'http' takes precedence over 'all://example.org' and 'all'
    expected = "http://proxy-scheme.local:3128"
    assert select_proxy(url, proxies) == expected