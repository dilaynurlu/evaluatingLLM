import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_simple_host():
    """
    Test that a URL consisting only of a hostname (with dots) gets the specified scheme prepended.
    The presence of dots prevents the hostname from being interpreted as a scheme.
    """
    url = "example.com"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://example.com"