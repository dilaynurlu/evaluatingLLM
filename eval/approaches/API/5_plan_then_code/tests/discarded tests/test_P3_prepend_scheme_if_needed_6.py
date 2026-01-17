import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_query_path_unicode():
    """
    Test that path and query parameters are preserved, including Unicode support.
    Refined to include:
    1. Standard path/query preservation.
    2. Internationalized Domain Names (IDN) and Unicode characters.
    """
    new_scheme = "http"
    
    # URL with Unicode host (café.com) and query param
    url = "café.com/search?q=€"
    expected = "http://café.com/search?q=€"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected