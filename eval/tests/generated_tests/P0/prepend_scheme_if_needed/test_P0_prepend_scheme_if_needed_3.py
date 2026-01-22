import pytest
from requests.utils import prepend_scheme_if_needed

def test_does_not_replace_existing_scheme():
    # Scenario: The URL already has a scheme (ftp).
    # The function should NOT replace it with the new_scheme (http).
    url = "ftp://ftp.example.com/pub"
    new_scheme = "http"
    
    # Execution
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Verification
    assert result == "ftp://ftp.example.com/pub"