import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ignores_existing_scheme():
    """
    Test that if a URL already has a scheme, the function returns it unchanged,
    ignoring the new_scheme argument.
    """
    url = "https://example.com"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com"