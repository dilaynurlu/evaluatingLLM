import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_does_not_replace_existing_scheme():
    """
    Test that the function does not modify the scheme if one is already present.
    """
    url = "ftp://files.example.com/upload"
    new_scheme = "http"
    
    # The existing scheme 'ftp' should be preserved, 'http' is ignored.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "ftp://files.example.com/upload"