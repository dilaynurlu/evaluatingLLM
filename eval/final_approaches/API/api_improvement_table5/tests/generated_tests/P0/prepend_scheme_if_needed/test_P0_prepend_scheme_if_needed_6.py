import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_query_and_path():
    """
    Test that path, query parameters, and fragments are preserved 
    when prepending a scheme.
    """
    url = "example.com/api/v1?search=test#fragment"
    new_scheme = "http"
    
    expected = "http://example.com/api/v1?search=test#fragment"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected