import pytest
from requests.auth import _basic_auth_str
import warnings

def test_basic_auth_str_int_username_deprecated():
    username = 12345
    password = "password"
    
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(username, password)
        
    expected_encoded = "MTIzNDU6cGFzc3dvcmQ=" # b64("12345:password")
    assert result == "Basic " + expected_encoded
