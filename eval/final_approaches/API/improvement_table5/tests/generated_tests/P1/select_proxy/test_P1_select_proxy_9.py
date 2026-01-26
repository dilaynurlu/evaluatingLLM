import pytest
from requests.utils import select_proxy

def test_select_proxy_port_exclusion_in_key():
    """
    Test that the proxy lookup key uses the hostname only (excluding the port).
    This confirms that a URL with a port will still match a proxy key defined
    as 'scheme://hostname'.
    """
    url = "http://example.com:8080/path"
    proxies = {
        "http://example.com": "http://correct-proxy",
        "all": "http://wrong-proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://correct-proxy"