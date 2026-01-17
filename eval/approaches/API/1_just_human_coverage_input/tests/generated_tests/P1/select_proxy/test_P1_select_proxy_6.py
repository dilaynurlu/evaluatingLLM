import pytest
from requests.utils import select_proxy

def test_select_proxy_no_hostname_fallback_all():
    """
    Test behavior when URL has no hostname and scheme is not in proxies.
    Should fallback to 'all'.
    """
    url = "file:///var/log/syslog"
    proxies = {
        "http": "http://web-proxy.local:8080",
        "all": "http://global-proxy.local:3128"
    }
    
    # urlparse('file:///...') results in hostname=None.
    # 'file' not in proxies, should return proxies['all']
    result = select_proxy(url, proxies)
    assert result == "http://global-proxy.local:3128"