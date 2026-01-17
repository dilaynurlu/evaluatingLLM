import pytest
from requests.utils import select_proxy

def test_select_proxy_all_host_match():
    """
    Test that select_proxy matches 'all://hostname' if specific scheme matches are missing.
    This corresponds to the 3rd priority in the lookup list.
    """
    url = "ftp://files.example.com/download"
    proxies = {
        "all://files.example.com": "http://files-proxy.local",
        "all": "http://global-proxy.local"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://files-proxy.local"