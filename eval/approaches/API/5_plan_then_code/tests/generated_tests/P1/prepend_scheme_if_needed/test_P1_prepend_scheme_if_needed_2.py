import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing():
    """
    Test that an existing scheme is NOT replaced by the new scheme.
    """
    url = "https://example.org/api"
    new_scheme = "http"
    
    # The function should detect the existing 'https' scheme and ignore 'http'
    expected = "https://example.org/api"
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected