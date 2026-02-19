import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_username_with_empty_password():
    """
    Test behavior when a username is provided with a colon but no password text.
    
    In this scenario, urlparse sets the password to an empty string (not None).
    unquote("") returns "", allowing the function to successfully return the username
    and an empty password, avoiding the exception fallback.
    """
    url = "http://user:@example.com/"
    expected_auth = ("user", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth