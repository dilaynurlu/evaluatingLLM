import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string_username_warning():
    """
    Test _basic_auth_str with a non-string/non-bytes username (e.g., int).
    
    This validates that a DeprecationWarning is issued and the integer is 
    converted to a string before encoding.
    
    Input: 12345 (int) : "password" (str)
    Effective Input: "12345:password"
    Base64: MTIzNDU6cGFzc3dvcmQ=
    """
    username = 12345
    password = "password"
    expected = "Basic MTIzNDU6cGFzc3dvcmQ="
    
    # We explicitly verify the warning, but ensure we capture the result
    # to verify the fallback logic correctness.
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(username, password)
    
    assert result == expected