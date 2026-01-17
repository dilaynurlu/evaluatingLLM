import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_path_and_query():
    """
    Test that a URL containing path and query parameters but no scheme
    gets the scheme prepended correctly, preserving the path and query.
    """
    url = "example.com/api/v1?search=foo&mode=bar"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com/api/v1?search=foo&mode=bar"