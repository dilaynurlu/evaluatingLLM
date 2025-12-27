import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_address():
    """
    Test that an IPv6 address literal without a scheme is correctly handled.
    """
    url = "[::1]:5000/status"
    new_scheme = "http"
    expected = "http://[::1]:5000/status"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected