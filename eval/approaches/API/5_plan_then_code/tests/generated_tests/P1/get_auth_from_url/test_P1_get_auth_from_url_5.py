import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username():
    """
    Test that a URL with an empty username (indicated by a leading colon in auth section)
    returns an empty string for the username and the correct password.
    """
    url = "http://:password@example.com/"
    expected_auth = ("", "password")
    
    assert get_auth_from_url(url) == expected_auth