import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_no_scheme():
    """
    Test that a URL without a scheme (and without //) gets the specified scheme prepended.
    This scenario typically causes the parser to treat the host as a path initially,
    triggering the 'netloc/path swap' logic in the function.
    """
    url = "example.com"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://example.com"