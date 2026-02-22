import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_ascii_credentials():
    """
    Test _basic_auth_str with simple ASCII username and password.
    """
    username = "user"
    password = "password"
    expected = "Basic dXNlcjpwYXNzd29yZA=="
    
    result = _basic_auth_str(username, password)
    assert result == expected
