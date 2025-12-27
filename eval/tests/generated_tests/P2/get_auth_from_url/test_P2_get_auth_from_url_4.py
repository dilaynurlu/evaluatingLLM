import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_invalid_input_type():
    """
    Test that passing a non-string input (e.g. None) triggers the internal exception handling
    and returns a tuple of empty strings instead of raising an error.
    """
    # urlparse(None) typically raises AttributeError or TypeError depending on implementation/version.
    # get_auth_from_url catches (AttributeError, TypeError) and returns ("", "").
    url = None
    expected_auth = ("", "")
    
    result = get_auth_from_url(url)
    
    assert result == expected_auth