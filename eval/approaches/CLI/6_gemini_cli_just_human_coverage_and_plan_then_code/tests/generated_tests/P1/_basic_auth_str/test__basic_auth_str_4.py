import pytest
from requests.auth import _basic_auth_str
import warnings

def test_basic_auth_str_int_password_deprecated():
    username = "user"
    password = 54321
    
    with pytest.warns(DeprecationWarning, match="Non-string passwords will no longer be supported"):
        result = _basic_auth_str(username, password)
        
    expected_encoded = "dXNlcjo1NDMyMQ==" # b64("user:54321")
    assert result == "Basic " + expected_encoded
