import pytest
from requests.utils import select_proxy

def test_select_proxy_precedence_order():
    """
    Test the full precedence order of proxy selection:
    1. scheme://hostname
    2. scheme
    3. all://hostname
    4. all
    """
    url = "http://test.example.com"
    
    # 1. Verify scheme://hostname wins over everything
    proxies_full = {
        "http://test.example.com": "winner-1",
        "http": "loser-2",
        "all://test.example.com": "loser-3",
        "all": "loser-4"
    }
    assert select_proxy(url, proxies_full) == "winner-1"
    
    # 2. Verify scheme wins when scheme://hostname is absent
    proxies_scheme = {
        "http": "winner-2",
        "all://test.example.com": "loser-3",
        "all": "loser-4"
    }
    assert select_proxy(url, proxies_scheme) == "winner-2"
    
    # 3. Verify all://hostname wins when scheme-specific keys are absent
    proxies_all_host = {
        "all://test.example.com": "winner-3",
        "all": "loser-4"
    }
    assert select_proxy(url, proxies_all_host) == "winner-3"