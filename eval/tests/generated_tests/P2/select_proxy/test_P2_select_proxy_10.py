import pytest
from requests.utils import select_proxy

def test_select_proxy_ignore_auth_in_key():
    """
    Test that username/password authentication in the URL is ignored
    when constructing the lookup key for the proxy.
    """
    url = "http://user:pass@auth.example.com/private"
    proxies = {
        "http://auth.example.com": "http://auth-proxy.local",
        "http": "http://general-proxy.local"
    }
    
    # Logic:
    # urlparse extracts hostname 'auth.example.com'
    # Key constructed: 'http://auth.example.com'
    expected = "http://auth-proxy.local"
    assert select_proxy(url, proxies) == expected