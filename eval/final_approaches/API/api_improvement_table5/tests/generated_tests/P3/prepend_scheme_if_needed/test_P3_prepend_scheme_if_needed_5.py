import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_path_query_fragment():
    """
    Test prepending a scheme to a URL string containing path, query, and fragment.
    
    This exercises the fallback logic for complex strings without schemes:
    1. 'example.com/resource?query=1#fragment' is parsed as a path (scheme=None, netloc=None).
    2. The function performs the path-to-netloc swap on the entire string.
    3. The result effectively treats the entire input as the authority/path block 
       to which the scheme is prefixed.
    """
    url = "example.com/resource?query=1#fragment"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com/resource?query=1#fragment"