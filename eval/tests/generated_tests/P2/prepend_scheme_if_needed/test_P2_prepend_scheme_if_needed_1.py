import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_simple_hostname():
    """
    Test that a simple hostname without a scheme gets the specified scheme prepended.
    This exercises the logic where netloc is initially missing/in path and gets swapped.
    """
    url = "example.com"
    new_scheme = "http"
    expected = "http://example.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected