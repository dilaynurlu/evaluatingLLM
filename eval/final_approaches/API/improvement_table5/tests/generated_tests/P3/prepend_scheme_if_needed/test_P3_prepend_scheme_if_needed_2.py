import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing():
    """
    Test that if a scheme is already present, it is preserved strictly.
    
    This verifies:
    1. The parser correctly identifies 'https' as the scheme.
    2. The 'if scheme is None' logic is skipped.
    3. The function returns the URL with its original scheme, ignoring the 'new_scheme' argument.
    """
    url = "https://example.com/api"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com/api"