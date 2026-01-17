import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_adds_scheme_to_netloc_starting_with_slashes():
    """
    Test that a new scheme is prepended to a protocol-relative URL (starting with //).
    """
    url = "//api.example.org/v1/resource"
    new_scheme = "https"
    
    # The function should identify the missing scheme and prepend the new one.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://api.example.org/v1/resource"