import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username_with_password():
    """
    Test extracting credentials when the username is empty but the password is provided.
    Format: http://:password@host
    """
    url = "https://:secretKey123@api.example.org"
    expected_auth = ("", "secretKey123")
    
    result = get_auth_from_url(url)
    
    assert result == expected_auth