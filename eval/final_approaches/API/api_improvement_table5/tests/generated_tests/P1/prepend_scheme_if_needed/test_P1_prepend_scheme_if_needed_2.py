import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing():
    """
    Test that if the URL already has a scheme, it is NOT replaced by the new scheme.
    """
    url = "https://example.com/foo"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com/foo"