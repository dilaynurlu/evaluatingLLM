import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_simple_host():
    """
    Test prepending a scheme to a simple hostname.
    The function should correctly prepend the new scheme.
    """
    url = "google.com"
    new_scheme = "http"
    
    # parse_url logic (via urllib3) handles 'google.com' by internally assuming it's a host 
    # (often by trying to parse it as such or by requests' usage).
    # Expected result is http://google.com
    expected = "http://google.com"
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected