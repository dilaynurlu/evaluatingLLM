import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth():
    """
    Test prepending a scheme to a protocol-relative URL that includes authentication.
    
    Security Note: Uses placeholder credentials to avoid triggering secret scanners.
    
    Logic verified:
    1. Input '//user:placeholder@db.local' parses with scheme=None but auth present.
    2. Netloc is identified as 'db.local' (no path/netloc swap needed).
    3. The function reconstructs the authority section by prepending auth to netloc.
    4. The new scheme is applied to the reconstructed URL.
    """
    url = "//user:placeholder@db.local"
    new_scheme = "postgres"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "postgres://user:placeholder@db.local"