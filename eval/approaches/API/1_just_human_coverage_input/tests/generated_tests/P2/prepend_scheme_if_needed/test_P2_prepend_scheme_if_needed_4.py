import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_supports_ipv6():
    """
    Test that an IPv6 address (with port) without a scheme gets the scheme prepended correctly.
    This ensures that the brackets and colons in IPv6 literals are handled properly 
    during parsing and reconstruction.
    """
    url = "[::1]:8080"
    new_scheme = "http"
    
    expected = "http://[::1]:8080"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == expected