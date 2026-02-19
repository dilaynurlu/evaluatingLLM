import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username_with_password():
    """
    Test behavior when a password is provided with an empty username (colon prefix).
    
    The function should correctly extract the empty username and the provided password.
    """
    url = "http://:secret@example.com/"
    expected_auth = ("", "secret")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth