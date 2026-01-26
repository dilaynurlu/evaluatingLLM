import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_ipv6_literal():
    """
    Test prepending a scheme to a URL containing an IPv6 literal and port.
    This ensures that bracketed hosts are handled correctly during reconstruction.
    """
    url = "[::1]:8080"
    new_scheme = "http"
    expected = "http://[::1]:8080"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected