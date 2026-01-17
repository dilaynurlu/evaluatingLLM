import pytest
from requests.utils import select_proxy

def test_select_proxy_no_match_found():
    """
    Test that select_proxy returns None when matches are found in the proxies dict.
    
    Refinement: Uses a valid URL structure but ensures safe return when keys don't match.
    """
    url = "http://example.com"
    proxies = {
        "https": "secure_proxy",
        "ftp": "ftp_proxy"
    }
    
    assert select_proxy(url, proxies) is None