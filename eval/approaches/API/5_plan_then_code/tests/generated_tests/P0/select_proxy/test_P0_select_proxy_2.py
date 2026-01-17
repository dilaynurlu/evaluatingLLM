import pytest
from requests.utils import select_proxy

def test_select_proxy_matches_specific_host():
    """
    Test that select_proxy prioritizes a specific 'scheme://hostname' key 
    over a general 'scheme' key.
    """
    url = "http://special.example.com/api"
    proxies = {
        "http": "http://general-proxy.com",
        "http://special.example.com": "http://special-proxy.com"
    }
    
    # Should match 'http://special.example.com' key
    result = select_proxy(url, proxies)
    assert result == "http://special-proxy.com"