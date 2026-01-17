import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_hostname():
    """
    Test that a simple hostname without a scheme gets the specified scheme prepended.
    """
    url = "google.com"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://google.com"