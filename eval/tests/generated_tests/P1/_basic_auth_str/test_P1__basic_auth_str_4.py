import pytest
import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_integer_username_deprecation():
    """
    Test _basic_auth_str with an integer username.
    Verifies that a DeprecationWarning is raised and the integer is converted to a string.
    """
    username = 12345
    password = "securepass"
    
    # The function checks isinstance(username, basestring).
    # Since int is not basestring, it warns and converts to str(username).
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(username, password)
    
    # Expect "12345:securepass"
    combined = str(username).encode("latin1") + b":" + password.encode("latin1")
    encoded_part = base64.b64encode(combined).decode("utf-8")
    expected_auth_str = f"Basic {encoded_part}"
    
    assert result == expected_auth_str