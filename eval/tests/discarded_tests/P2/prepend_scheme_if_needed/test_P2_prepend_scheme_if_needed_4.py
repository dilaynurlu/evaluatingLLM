import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ignores_ambiguous_auth():
    """
    Test that a URL starting with 'user:pass@...' is NOT modified.
    
    The parser treats the 'user' part before the colon as the scheme. 
    Since a scheme is detected (even if it was intended as a username), 
    prepend_scheme_if_needed should consider the URL as already having a scheme 
    and make no changes.
    """
    url = "user:password@example.com"
    new_scheme = "https"
    expected = "user:password@example.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected