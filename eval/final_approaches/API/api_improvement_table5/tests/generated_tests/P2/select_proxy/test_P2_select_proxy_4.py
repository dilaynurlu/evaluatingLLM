import pytest
from requests.utils import select_proxy

def test_select_proxy_fallback_to_all_when_hostname_is_none():
    """
    Test that select_proxy falls back to the 'all' key when the URL does not 
    contain a hostname and the specific scheme is not in the proxies dictionary.
    """
    url = "file:///etc/hosts"
    proxies = {
        "http": "http://http.proxy",
        "all": "http://fallback.proxy"
    }
    
    # 'file' scheme is not in proxies, should fallback to 'all'
    result = select_proxy(url, proxies)
    
    assert result == "http://fallback.proxy"