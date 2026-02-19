import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_complex_components():
    """
    Test prepending scheme to a URL string that includes path, query, and fragment.
    This ensures that all components are preserved correctly during reconstruction.
    """
    url = "example.com/path/to/resource?query=param#fragment"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com/path/to/resource?query=param#fragment"