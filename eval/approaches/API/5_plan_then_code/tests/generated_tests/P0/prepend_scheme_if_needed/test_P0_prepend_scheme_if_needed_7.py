import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_ipv6_literal():
    """
    Test that an IPv6 address literal gets the scheme prepended.
    IPv6 literals usually start with '[' which is not a valid scheme start character.
    """
    url = "[::1]"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://[::1]"