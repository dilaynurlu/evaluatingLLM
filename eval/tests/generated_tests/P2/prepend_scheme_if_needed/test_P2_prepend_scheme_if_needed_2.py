import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing_scheme():
    """
    Test that the function does not modify a URL that already has a valid scheme,
    even if it differs from the new_scheme argument.
    """
    url = "ftp://example.com/resource"
    new_scheme = "http"
    expected = "ftp://example.com/resource"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected