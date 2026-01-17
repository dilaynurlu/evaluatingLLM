import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_handles_protocol_relative_auth():
    """
    Test that a protocol-relative URL (starting with //) containing authentication info
    correctly receives the new scheme. 
    
    This specifically targets the case where 'user:pass@...' might be misparsed as 
    scheme='user' if the leading '//' were omitted.
    """
    # '//' ensures the parser treats the following part as netloc/authority
    url = "//user:pass@db.internal"
    new_scheme = "postgres"
    
    expected = "postgres://user:pass@db.internal"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == expected