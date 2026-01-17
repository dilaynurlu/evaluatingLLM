import pytest
from requests.utils import select_proxy

def test_select_proxy_capitalized_url():
    """
    Test that select_proxy handles uppercase characters in the URL scheme and hostname correctly.
    
    It should normalize them to lowercase before looking up in the proxies dictionary.
    """
    url = "HTTP://EXAMPLE.COM/path"
    
    # Proxies keys are conventionally lowercase.
    proxies = {
        "http://example.com": "http://lowercase.proxy",
    }
    
    result = select_proxy(url, proxies)
    
    assert result == "http://lowercase.proxy"