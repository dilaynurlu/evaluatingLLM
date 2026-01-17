import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_query_and_fragment():
    """
    Test that URL path, query parameters, and fragments are preserved intact
    when a scheme is prepended.
    """
    url = "api.example.com/v1/search?q=test&page=1#results"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://api.example.com/v1/search?q=test&page=1#results"