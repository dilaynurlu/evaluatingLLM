import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_literal():
    """
    Test prepending a scheme to a URL containing an IPv6 literal and port.
    
    This ensures robustness in parsing complex hosts:
    1. '[::1]:8080' is correctly identified as the host/netloc.
    2. Brackets and port numbers are preserved during reconstruction.
    3. The scheme is prepended without altering the IPv6 syntax.
    """
    url = "//[::1]:8080"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://[::1]:8080"