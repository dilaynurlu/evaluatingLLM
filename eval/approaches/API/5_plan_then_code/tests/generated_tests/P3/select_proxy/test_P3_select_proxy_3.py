import pytest
from requests.utils import select_proxy

def test_select_proxy_all_host_priority_over_all():
    """
    Test that 'all://hostname' takes precedence over generic 'all'.
    
    Refinement: Uses a URL containing user authentication (user:pass) to verify
    that credentials are stripped from the hostname before key lookup.
    """
    # URL with authentication credentials
    url = "http://user:pass@example.com/resource"
    proxies = {
        # Missing http-specific keys
        "all://example.com": "all_host_proxy",
        "all": "all_proxy",
    }
    
    # Expect match on all://hostname, confirming auth was stripped
    assert select_proxy(url, proxies) == "all_host_proxy"