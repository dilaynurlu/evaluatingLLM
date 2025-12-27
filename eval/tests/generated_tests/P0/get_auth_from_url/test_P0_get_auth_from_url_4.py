import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password_field():
    """
    Test extraction when the password field is explicitly empty but the delimiter exists.
    'user:@host' results in username='user' and password=''.
    This differs from 'user@host' where password is None.
    """
    url = "http://myuser:@example.com/data"
    expected_auth = ("myuser", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth