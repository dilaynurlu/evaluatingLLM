import pytest
from requests.utils import select_proxy

def test_select_proxy_url_with_auth_credentials():
    """
    Test that URLs containing authentication credentials still match
    proxies defined for the hostname.
    """
    url = "https://user:password@secret.example.com/resource"
    proxies = {
        "https://secret.example.com": "http://auth-aware-proxy.local:3128"
    }
    
    # urlparse extracts 'secret.example.com' as hostname, ignoring user:password
    result = select_proxy(url, proxies)
    assert result == "http://auth-aware-proxy.local:3128"