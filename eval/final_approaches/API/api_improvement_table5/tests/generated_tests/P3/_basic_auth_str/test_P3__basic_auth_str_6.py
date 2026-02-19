import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string_password_warning():
    """
    Test _basic_auth_str with a non-string/non-bytes password (e.g., None).
    
    This validates that a DeprecationWarning is issued and None is converted 
    to the string "None".
    
    Input: "user" (str) : None (NoneType)
    Effective Input: "user:None"
    Base64: dXNlcjpOb25l
    """
    username = "user"
    password = None
    expected = "Basic dXNlcjpOb25l"
    
    with pytest.warns(DeprecationWarning, match="Non-string passwords will no longer be supported"):
        result = _basic_auth_str(username, password)
    
    assert result == expected