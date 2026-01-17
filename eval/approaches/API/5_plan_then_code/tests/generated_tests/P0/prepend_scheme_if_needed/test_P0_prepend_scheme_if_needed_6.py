import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_ipv4_literal():
    """
    Test that an IPv4 address literal gets the scheme prepended.
    IPv4 addresses contain dots but no colon at the end of the first segment, so no scheme is detected.
    """
    url = "192.168.1.1"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://192.168.1.1"