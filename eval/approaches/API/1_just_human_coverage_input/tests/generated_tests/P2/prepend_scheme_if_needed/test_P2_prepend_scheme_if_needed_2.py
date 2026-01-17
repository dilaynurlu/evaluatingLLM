import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_ignores_existing_scheme():
    """
    Test that if the URL already has a scheme, it is NOT replaced by the new_scheme.
    The function should return the original URL unchanged.
    """
    url = "http://example.com"
    new_scheme = "https"
    
    # The existing scheme 'http' should be preserved; 'https' is ignored.
    expected = "http://example.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == expected