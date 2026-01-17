import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_order():
    """
    Test that select_proxy respects the precedence order:
    1. scheme://hostname
    2. scheme
    3. all://hostname
    4. all
    
    Refinement: Also verifies that the URL scheme and hostname are treated case-insensitively
    during the lookup (e.g., HTTP://EXAMPLE.COM matches http://example.com).
    """
    # URL with uppercase scheme and hostname to test normalization
    url = "HTTP://EXAMPLE.COM/resource"
    proxies = {
        "http://example.com": "http_host_proxy",
        "http": "http_scheme_proxy",
        "all://example.com": "all_host_proxy",
        "all": "all_proxy",
    }
    
    # Expect the most specific match (scheme://hostname) despite case difference in URL
    assert select_proxy(url, proxies) == "http_host_proxy"