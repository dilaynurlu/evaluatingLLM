import pytest
from requests.utils import select_proxy

def test_select_proxy_handles_mixed_case_url():
    """
    Test that the function normalizes the URL hostname and scheme to lowercase
    before looking up keys in the proxies dictionary.
    
    The URL provided has mixed case scheme and host, but the proxy dictionary
    uses lowercase keys.
    """
    url = "HTTP://My-Server.COM/path"
    proxies = {
        "http://my-server.com": "http://matched-proxy.local",
        "all": "http://wrong-proxy.local",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://matched-proxy.local"