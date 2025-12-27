import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed bytes and string inputs.
    Verifies that the function correctly handles combining a string username (encoded to latin1)
    and a bytes password.
    """
    username = "user"    # string
    password = b"secret" # bytes
    
    # 'user' -> b'user'
    # b'secret' -> b'secret'
    # Joined: b'user:secret' -> b64 -> b'dXNlcjpzZWNyZXQ='
    expected_auth_str = "Basic dXNlcjpzZWNyZXQ="
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str