import pytest
from requests.utils import select_proxy

def test_select_proxy_case_insensitivity_normalization():
    """
    Test that select_proxy relies on urlparse normalization, so upper-case
    URLs match lower-case keys in the proxy dictionary.
    """
    # Upper case URL scheme and host
    url = "HTTP://UPPER.EXAMPLE.COM/PATH"
    
    # Proxies dictionary keys are typically lowercase.
    # select_proxy does not normalize the dict keys, but it constructs
    # the lookup key from normalized url parts.
    proxies = {
        "http://upper.example.com": "http://matched.local",
        "http": "http://general.local"
    }
    
    # Logic:
    # urlparse("HTTP://...") -> scheme='http', hostname='upper.example.com'
    # Key constructed: 'http://upper.example.com'
    expected = "http://matched.local"
    assert select_proxy(url, proxies) == expected