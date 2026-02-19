import pytest
from requests.utils import select_proxy

def test_select_proxy_priority_all_host():
    """
    Test the third priority match: all://hostname.
    It should take precedence over 'all', when specific scheme matches are missing.
    """
    url = "http://example.com/resource"
    proxies = {
        "all://example.com": "http://all-host.proxy",
        "all": "http://all.proxy",
        "ftp": "http://ftp.proxy"  # Irrelevant scheme
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://all-host.proxy"