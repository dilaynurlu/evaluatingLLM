import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password():
    """
    Test that a URL with a username and an empty password (indicated by a trailing colon)
    returns the username and an empty string for the password.
    """
    url = "http://user:@example.com/"
    expected_auth = ("user", "")
    
    assert get_auth_from_url(url) == expected_auth