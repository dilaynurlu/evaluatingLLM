import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_simple_host():
    """
    Test prepending a scheme to a simple hostname URL.
    This validates the basic functionality and the internal logic that handles
    missing netlocs by checking if the parser placed the host in the path.
    """
    url = "example.com"
    new_scheme = "https"
    expected = "https://example.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected