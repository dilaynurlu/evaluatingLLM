import pytest
from requests.utils import get_auth_from_url

def test_get_auth_empty_password_field():
    """
    Test extracting auth when the password field is empty but the colon separator exists.
    Format: http://user:@host
    """
    url = "ftp://myuser:@ftp.example.com"
    expected_auth = ("myuser", "")
    
    assert get_auth_from_url(url) == expected_auth