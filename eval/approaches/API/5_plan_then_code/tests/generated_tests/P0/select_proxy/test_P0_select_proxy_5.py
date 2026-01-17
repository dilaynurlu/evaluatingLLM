import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallbacks_to_all():
    """
    Test that URLs without a hostname fallback to 'all' if the scheme 
    is not found in the proxies dictionary.
    """
    url = "file:///var/log/syslog"
    proxies = {
        "http": "http://http-proxy.com",
        "all": "http://universal-proxy.com"
    }
    
    # hostname is None, scheme 'file' not in proxies -> fallback to 'all'
    result = select_proxy(url, proxies)
    assert result == "http://universal-proxy.com"