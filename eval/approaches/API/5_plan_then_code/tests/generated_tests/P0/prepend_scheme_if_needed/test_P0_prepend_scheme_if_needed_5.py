import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_auth_url():
    """
    Test that a URL with authentication information gets the scheme prepended correctly.
    We use '//' prefix to ensure the parser treats 'user' as part of authority, not as a scheme.
    The function handles reconstructing the netloc with auth.
    """
    url = "//user:password@example.com"
    new_scheme = "ftps"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "ftps://user:password@example.com"