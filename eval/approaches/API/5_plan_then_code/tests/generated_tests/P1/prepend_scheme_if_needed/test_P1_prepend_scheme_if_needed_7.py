import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_explicit_port():
    """
    Test prepending a scheme to a host:port pair.
    This ensures the presence of a port doesn't confuse the scheme detection.
    """
    url = "google.com:8080"
    new_scheme = "http"
    
    # google.com:8080 does not look like a scheme (dot in first segment), 
    # so it should be treated as netloc.
    expected = "http://google.com:8080"
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected