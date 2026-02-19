import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_host_and_path():
    """
    Test prepending scheme to a URL consisting of a host and path.
    The parser initially treats 'example.com/foo' as a path (due to missing //), 
    so the function should swap it to netloc and prepend the scheme.
    """
    url = "example.com/foo/bar"
    new_scheme = "http"
    
    # Expected behavior: scheme is added, 'example.com' is treated as host
    expected = "http://example.com/foo/bar"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected