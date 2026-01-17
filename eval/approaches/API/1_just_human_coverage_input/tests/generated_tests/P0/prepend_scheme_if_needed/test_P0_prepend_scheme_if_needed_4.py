import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_handles_authentication_in_netloc():
    """
    Test that authentication information in the URL is correctly preserved/reconstructed
    when prepending a scheme.
    """
    # Using a protocol-relative URL to ensure parsing treats 'user:pass' as auth
    # rather than a scheme.
    url = "//user:password@internal.service.local"
    new_scheme = "https"
    
    # The function has specific logic to reconstruct netloc with auth.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://user:password@internal.service.local"