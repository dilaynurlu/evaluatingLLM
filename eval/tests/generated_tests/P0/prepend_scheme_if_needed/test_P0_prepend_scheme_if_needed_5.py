import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_netloc_with_auth():
    # Scenario: Input URL includes username/password and host (netloc-relative).
    # Using '//' ensures the parser correctly identifies the authority section.
    url = "//user:password@internal.service"
    new_scheme = "https"
    
    # Execution
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Verification
    # The function handles auth separation in parsing and must reconstruct it correctly.
    assert result == "https://user:password@internal.service"