import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_host():
    """
    Test prepending scheme to an IPv6 address literal.
    Using '//' prefix to ensure it is treated as a netloc.
    """
    url = "//[::1]:8080"
    new_scheme = "https"
    
    expected = "https://[::1]:8080"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected