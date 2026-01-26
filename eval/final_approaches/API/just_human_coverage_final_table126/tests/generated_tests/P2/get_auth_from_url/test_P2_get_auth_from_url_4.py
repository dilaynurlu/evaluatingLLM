import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_colon_in_password():
    """
    Test extraction when the password itself contains a colon.
    The first colon separates user and password; subsequent colons belong to the password.
    """
    # User: "user"
    # Password: "password:with:colons"
    url = "ftp://user:password:with:colons@example.com/"
    expected_auth = ("user", "password:with:colons")
    
    assert get_auth_from_url(url) == expected_auth