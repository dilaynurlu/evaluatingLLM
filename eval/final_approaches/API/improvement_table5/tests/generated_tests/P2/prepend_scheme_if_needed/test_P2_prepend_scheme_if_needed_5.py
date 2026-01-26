import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_literal():
    """
    Test prepending scheme to an IPv6 literal address.
    Ensures that the brackets and port handling works correctly during reconstruction.
    """
    url = "[::1]:8000/status"
    new_scheme = "http"
    
    expected = "http://[::1]:8000/status"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected