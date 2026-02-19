import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_auth_handling():
    """
    Test handling of URLs with authentication information.
    We use a protocol-relative URL '//' to ensure the parser correctly identifying
    the authority section without confusing the user/pass as a scheme.
    """
    url = "//user:pass@example.com"
    new_scheme = "ftp"
    
    # The function should detect the auth component and reconstruct the netloc correctly
    # combining auth and host.
    expected = "ftp://user:pass@example.com"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected