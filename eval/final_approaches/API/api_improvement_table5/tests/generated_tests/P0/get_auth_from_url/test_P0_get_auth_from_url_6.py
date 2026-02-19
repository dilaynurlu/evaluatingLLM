import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_incomplete_auth_user_only():
    """
    Test extracting auth when only username is provided without a password separator.
    URL format: user@host
    
    In this scenario, urlparse usually sets username='user' and password=None.
    The unquote(None) call for password raises TypeError.
    The function catches TypeError and returns ('', '').
    """
    url = "http://onlyuser@example.com"
    auth = get_auth_from_url(url)
    
    assert auth == ("", "")