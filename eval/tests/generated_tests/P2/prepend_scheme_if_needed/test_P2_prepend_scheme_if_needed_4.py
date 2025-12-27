import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_starting_with_double_slash():
    """
    Test that a URL starting with double slashes (protocol-relative URL)
    gets the scheme prepended correctly without duplicating slashes or netloc.
    """
    url = "//cdn.example.org/assets/style.css"
    new_scheme = "https"
    expected = "https://cdn.example.org/assets/style.css"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected