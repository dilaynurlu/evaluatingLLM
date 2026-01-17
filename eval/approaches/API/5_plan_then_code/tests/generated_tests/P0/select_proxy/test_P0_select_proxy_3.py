import pytest
from requests.utils import select_proxy

def test_select_proxy_matches_all_key():
    """
    Test that select_proxy falls back to the 'all' key when neither 
    the specific host nor the scheme keys are present in the proxies dictionary.
    """
    url = "ftp://files.example.com/download"
    proxies = {
        "http": "http://http-proxy.com",
        "all": "socks5://fallback-proxy.com"
    }
    
    # 'ftp' scheme not in proxies, so should fallback to 'all'
    result = select_proxy(url, proxies)
    assert result == "socks5://fallback-proxy.com"