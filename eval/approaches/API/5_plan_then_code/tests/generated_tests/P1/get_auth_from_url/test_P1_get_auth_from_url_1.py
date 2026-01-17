import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_valid_credentials():
    """
    Test that a URL with standard username and password components
    is correctly parsed into an auth tuple.
    """
    url = "http://user:password@example.com/"
    expected_auth = ("user", "password")
    
    assert get_auth_from_url(url) == expected_auth