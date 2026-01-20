from requests.auth import _basic_auth_str
import pytest
import warnings
import base64

def test_basic_auth_str_non_string_password():
    username = "user"
    password = 456
    
    with pytest.warns(DeprecationWarning, match="Non-string passwords will no longer be supported"):
        result = _basic_auth_str(username, password)
    
    expected_token = base64.b64encode(b"user:456").decode("utf-8")
    assert result == f"Basic {expected_token}"
