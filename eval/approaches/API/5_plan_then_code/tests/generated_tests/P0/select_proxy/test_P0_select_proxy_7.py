import pytest
from requests.utils import select_proxy

def test_select_proxy_ignores_port_in_lookup_key():
    """
    Test that select_proxy generates lookup keys based on hostname only,
    ignoring the port number in the URL.
    """
    url = "http://example.com:8080/path"
    # The function extracts hostname 'example.com'
    # It should look for 'http://example.com', not 'http://example.com:8080'
    proxies = {
        "http://example.com": "http://host-match.proxy",
        "http://example.com:8080": "http://port-match.proxy"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://host-match.proxy"