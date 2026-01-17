from requests.auth import _basic_auth_str
import pytest
import warnings
import base64

def test_basic_auth_str_non_string_username():
    username = 123
    password = "password"
    
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(username, password)
    
    # 123 becomes "123"
    expected_token = base64.b64encode(b"123:password").decode("utf-8")
    assert result == f"Basic {expected_token}"
