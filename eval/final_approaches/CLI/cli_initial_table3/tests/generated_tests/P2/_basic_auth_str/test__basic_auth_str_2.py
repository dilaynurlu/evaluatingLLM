import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_empty_strings():
    """
    Test _basic_auth_str with empty username and password.
    """
    username = ""
    password = ""
    expected = "Basic Og=="  # base64.b64encode(b":")
    
    result = _basic_auth_str(username, password)
    assert result == expected
