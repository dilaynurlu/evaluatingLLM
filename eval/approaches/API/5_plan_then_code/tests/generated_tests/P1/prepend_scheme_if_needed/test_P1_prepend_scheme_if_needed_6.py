import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_host_and_path():
    """
    Test prepending a scheme to a URL consisting of a host and path (without //).
    """
    url = "example.com/foo"
    new_scheme = "https"
    
    expected = "https://example.com/foo"
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected