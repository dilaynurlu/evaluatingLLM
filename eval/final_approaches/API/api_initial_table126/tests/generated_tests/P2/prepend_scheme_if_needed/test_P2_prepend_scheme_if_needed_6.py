import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_path_and_query():
    """
    Test prepending a scheme to a domain-like string followed by a path and query.
    
    This scenario often results in the parser initially placing the entire string 
    into the 'path' component. The function must detect the missing netloc, 
    swap the path to netloc, and correctly reconstruct the full URL including the query.
    """
    url = "api.example.com/v1/search?q=test&lang=en"
    new_scheme = "https"
    expected = "https://api.example.com/v1/search?q=test&lang=en"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected