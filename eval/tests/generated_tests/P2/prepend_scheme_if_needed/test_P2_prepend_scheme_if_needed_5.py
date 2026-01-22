import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_protocol_relative_with_auth():
    """
    Test prepending a scheme to a protocol-relative URL that includes authentication.
    
    Input starting with '//' allows the parser to correctly identify the authority 
    section (user:pass@host) without confusing the user part for a scheme.
    This specifically exercises the logic that reconstructs the netloc with auth info.
    """
    url = "//user:pass@db.internal:5432/db"
    new_scheme = "postgresql"
    expected = "postgresql://user:pass@db.internal:5432/db"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected