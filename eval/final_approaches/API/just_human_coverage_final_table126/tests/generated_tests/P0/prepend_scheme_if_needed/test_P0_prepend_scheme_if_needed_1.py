import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_host_only():
    # Scenario: Input is a plain hostname without scheme.
    # The function should prepend the provided scheme.
    url = "google.com"
    new_scheme = "http"
    
    # Execution
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Verification
    # parse_url identifies 'google.com' as the host (likely via internal // prefixing),
    # so prepend_scheme_if_needed applies the new scheme to it.
    assert result == "http://google.com"