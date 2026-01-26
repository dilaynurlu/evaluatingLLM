import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_simple_host():
    """
    Test prepending a scheme to a simple host URL.
    The function should interpret 'example.com' as a host (netloc) 
    and prepend the new scheme.
    """
    url = "example.com"
    new_scheme = "http"
    
    # "example.com" is parsed as host="example.com" by requests' internal logic
    # (via urllib3.util.parse_url which adds // if scheme is missing)
    expected = "http://example.com"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected