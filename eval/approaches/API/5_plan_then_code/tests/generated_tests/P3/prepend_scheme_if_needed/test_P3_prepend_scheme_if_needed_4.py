import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_literal():
    """
    Test prepending a scheme to an IPv6 literal address with a port.
    Verifies that the bracketed notation is preserved correctly.
    """
    url = "[::1]:8080"
    new_scheme = "http"
    expected = "http://[::1]:8080"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected