import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_basic_host():
    """
    Test that a simple hostname without a scheme gets the scheme prepended.
    
    This verifies the 'missing netloc' workaround:
    1. 'google.com' is initially parsed as a path, with no netloc.
    2. The function detects the missing netloc and swaps the path ('google.com') 
       into the netloc position.
    3. The provided scheme is applied, resulting in a valid URL.
    """
    url = "google.com"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://google.com"