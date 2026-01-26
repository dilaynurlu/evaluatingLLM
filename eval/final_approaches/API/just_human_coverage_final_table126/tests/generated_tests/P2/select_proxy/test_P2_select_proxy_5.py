import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_scheme_over_all_host():
    """
    Test the precedence rule where a generic scheme proxy ('http')
    should be selected over a host-specific 'all' proxy ('all://hostname').
    """
    url = "http://priority.example.com/"
    proxies = {
        "http": "http://scheme-winner.local",
        "all://priority.example.com": "http://host-loser.local",
        "all": "http://global-loser.local"
    }
    
    # Order of checks:
    # 1. http://priority.example.com (missing)
    # 2. http (present) -> Match!
    # 3. all://priority.example.com
    # 4. all
    expected = "http://scheme-winner.local"
    assert select_proxy(url, proxies) == expected