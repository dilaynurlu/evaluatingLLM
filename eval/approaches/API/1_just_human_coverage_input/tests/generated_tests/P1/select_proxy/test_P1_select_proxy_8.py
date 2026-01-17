import pytest
from requests.utils import select_proxy

def test_select_proxy_ipv6_hostname():
    """
    Test that IPv6 hostnames are handled correctly.
    Note: urlparse returns IPv6 hostnames without brackets for .hostname.
    """
    url = "http://[::1]/index.html"
    # Logic: keys constructed as scheme + "://" + hostname
    # hostname for [::1] is ::1
    proxies = {
        "http://::1": "http://ipv6-proxy.local:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://ipv6-proxy.local:8080"