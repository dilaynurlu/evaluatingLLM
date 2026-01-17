import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_protocol_relative():
    """
    Test that a protocol-relative URL (starting with //) containing authentication
    information gets the scheme prepended correctly. This verifies that the auth
    information is preserved and correctly integrated into the netloc.
    """
    # Using '//' prefix ensures it is parsed as a netloc with auth, 
    # rather than treating 'user' as the scheme.
    url = "//user:pass@db.internal:5432"
    new_scheme = "postgresql"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "postgresql://user:pass@db.internal:5432"