import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_adds_scheme_to_host():
    """
    Test that a URL consisting only of a hostname gets the specified scheme prepended.
    This validates the primary functionality: converting 'host' to 'scheme://host'.
    """
    url = "example.com"
    new_scheme = "https"
    expected = "https://example.com"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == expected