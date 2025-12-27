import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing_scheme():
    """
    Test that if a URL already has a scheme, it is preserved and the new scheme is ignored.
    """
    url = "https://example.com/foo"
    new_scheme = "http"
    expected = "https://example.com/foo"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected