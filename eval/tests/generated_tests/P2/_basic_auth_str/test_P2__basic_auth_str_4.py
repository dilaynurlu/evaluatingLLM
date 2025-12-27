import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_warning_username():
    """
    Test that passing a non-basestring (e.g., int) username triggers a DeprecationWarning
    and correctly converts the input to a string before encoding.
    """
    username = 12345
    password = "password"
    
    # "12345:password" -> b64 -> "Basic MTIzNDU6cGFzc3dvcmQ="
    expected_auth_str = "Basic MTIzNDU6cGFzc3dvcmQ="
    
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(username, password)
        
    assert result == expected_auth_str