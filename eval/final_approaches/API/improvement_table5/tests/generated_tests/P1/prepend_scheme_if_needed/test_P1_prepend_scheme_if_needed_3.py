import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_protocol_relative_with_auth():
    """
    Test prepending scheme to a protocol-relative URL that includes authentication.
    This explicitly targets the 'if auth:' block where netloc is reconstructed
    because parse_url separates auth from netloc.
    Input starting with '//' ensures parse_url identifies it as authority, not path.
    """
    url = "//user:pass@example.com:8080/path"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # parse_url separates auth, so the function reconstructs it: user:pass@example.com:8080
    assert result == "https://user:pass@example.com:8080/path"