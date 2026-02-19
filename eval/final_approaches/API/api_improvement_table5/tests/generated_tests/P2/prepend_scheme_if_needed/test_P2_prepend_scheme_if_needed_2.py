import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing_scheme():
    """
    Test that an existing scheme is NOT replaced.
    If the URL already starts with a scheme, the function should simply return it 
    (possibly normalized, but with the original scheme).
    """
    url = "https://example.com/api"
    new_scheme = "http"
    
    # Expected behavior: URL remains unchanged as it already has a scheme
    expected = "https://example.com/api"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected