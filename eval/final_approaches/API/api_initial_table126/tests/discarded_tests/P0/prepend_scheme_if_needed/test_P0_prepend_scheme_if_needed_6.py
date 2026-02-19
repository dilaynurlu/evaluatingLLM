import pytest
from requests.utils import prepend_scheme_if_needed

def test_treats_auth_prefix_as_scheme_without_slashes():
    # Scenario: Input 'user:pass@host' lacks '//'.
    # Standard parsers (RFC 3986) treat the first token 'user:' as a scheme, not a username.
    # Therefore, the function sees a URL *with* a scheme ('user') and does NOT prepend 'http'.
    url = "user:pass@host"
    new_scheme = "http"
    
    # Execution
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Verification
    # The original scheme 'user' is preserved.
    # Note: The function's internal swap logic for missing netlocs will coerce the path 
    # 'pass@host' into the netloc position, adding '//' in the output.
    # Input 'user:pass@host' -> scheme='user', path='pass@host' -> swap -> scheme='user', netloc='pass@host'
    # Result -> 'user://pass@host'
    assert result == "user://pass@host"