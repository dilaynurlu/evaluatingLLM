import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password_field():
    """
    Test extracting auth when the password field is present but empty.
    URL format: user:@host
    'username' should be 'user', 'password' should be an empty string (not None).
    """
    url = "http://myuser:@example.com"
    auth = get_auth_from_url(url)
    
    # In this case, urlparse returns password='', so unquote('') -> ''
    # No exception should be raised.
    assert auth == ("myuser", "")