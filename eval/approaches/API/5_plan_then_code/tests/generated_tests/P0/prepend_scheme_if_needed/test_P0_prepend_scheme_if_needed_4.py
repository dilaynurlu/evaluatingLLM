import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_url_with_port():
    """
    Test that a URL with a hostname and port (and dots in hostname) gets the scheme prepended.
    The dots ensure 'example.com' is not seen as a scheme 'example.com:'.
    """
    url = "example.com:8080"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://example.com:8080"