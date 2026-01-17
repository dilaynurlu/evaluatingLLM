import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_non_string_input():
    """
    Test that passing a non-string object (e.g. integer) that is not None
    also results in an empty tuple due to exception handling.
    """
    invalid_input = 123456
    expected_auth = ("", "")
    
    assert get_auth_from_url(invalid_input) == expected_auth