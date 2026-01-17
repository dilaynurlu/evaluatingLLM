import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_preserves_path_query_fragment():
    """
    Test that adding a scheme to a URL string that includes path, query parameters, 
    and a fragment identifier preserves all those components exactly.
    """
    url = "api.example.com/v1/resource?active=true&sort=desc#ref-1"
    new_scheme = "https"
    
    expected = "https://api.example.com/v1/resource?active=true&sort=desc#ref-1"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == expected