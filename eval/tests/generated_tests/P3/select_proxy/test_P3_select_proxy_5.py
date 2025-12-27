import pytest
from requests.utils import select_proxy

def test_select_proxy_scheme_only_file_url():
    """
    Refined test for URLs without hostnames (e.g. file://).
    Verifies that the selector can handle URLs where netloc is empty 
    and match based on the scheme alone.
    """
    # file:// URL often has empty netloc (file:///path)
    url = "file:///etc/hosts"
    proxies = {
        "file": "http://proxy.file-server:8080",
        "all": "http://proxy.fallback:8080"
    }
    
    result = select_proxy(url, proxies)
    assert result == "http://proxy.file-server:8080"