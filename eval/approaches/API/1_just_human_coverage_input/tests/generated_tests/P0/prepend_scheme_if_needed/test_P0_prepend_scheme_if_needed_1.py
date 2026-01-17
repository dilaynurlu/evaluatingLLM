import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_adds_scheme_to_host_string():
    """
    Test that a new scheme is prepended to a URL string that only contains a host.
    """
    url = "example.com"
    new_scheme = "http"
    
    # When a bare host is provided, requests logic (via parse_url which may auto-fix 
    # the input or the swap logic in the function) should result in a valid URL with the scheme.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://example.com"