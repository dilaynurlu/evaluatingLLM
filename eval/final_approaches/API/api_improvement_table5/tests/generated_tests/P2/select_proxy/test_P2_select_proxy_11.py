import pytest
from requests.utils import select_proxy

def test_select_proxy_url_case_insensitivity():
    """
    Test that the URL is normalized (lowercased scheme and host) before lookup.
    Proxies dictionary keys are expected to be lowercase.
    """
    # Mixed case URL
    url = "HTTP://EXAMPLE.COM/Path"
    
    proxies = {
        "http://example.com": "http://normalized.proxy"
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://normalized.proxy"