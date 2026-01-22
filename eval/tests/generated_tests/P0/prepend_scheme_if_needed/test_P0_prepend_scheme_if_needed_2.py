import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_host_with_path_and_query():
    # Scenario: Input contains host, path, and query params but no scheme.
    url = "example.org/api/search?q=pytest"
    new_scheme = "https"
    
    # Execution
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Verification
    # The scheme is prepended, preserving the rest of the structure.
    assert result == "https://example.org/api/search?q=pytest"