import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_full_url_components():
    """
    Test a complex URL without a scheme containing port, path, query parameters, 
    and fragment identifier to ensure all components are preserved during reconstruction.
    """
    url = "api.service.io:8080/v1/data?filter=active&sort=desc#section2"
    new_scheme = "http"
    expected = "http://api.service.io:8080/v1/data?filter=active&sort=desc#section2"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected