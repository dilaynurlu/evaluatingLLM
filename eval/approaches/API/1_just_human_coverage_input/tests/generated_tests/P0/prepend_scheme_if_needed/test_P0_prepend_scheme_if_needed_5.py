import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_handles_ipv6_literal_with_port():
    """
    Test that IPv6 literals with ports are handled correctly when prepending a scheme.
    """
    url = "//[::1]:8080/status"
    new_scheme = "http"
    
    # IPv6 addresses in brackets should be preserved in the netloc.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://[::1]:8080/status"