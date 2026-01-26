import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_existing_scheme():
    """
    Test that if a scheme is already present, it is NOT replaced.
    """
    url = "https://example.com"
    new_scheme = "http"
    
    # The existing scheme 'https' should take precedence over 'http'
    expected = "https://example.com"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected