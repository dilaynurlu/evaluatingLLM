import pytest
from requests.utils import get_auth_from_url

def test_get_auth_user_without_password_separator():
    """
    Test behavior when only a username is provided without a colon separator.
    
    In standard urlparse, this results in username='user' and password=None.
    The get_auth_from_url function attempts to unquote both. Since unquote(None)
    raises a TypeError, the function catches it and returns ("", "").
    """
    url = "http://admin@dashboard.local"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth