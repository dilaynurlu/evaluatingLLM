from requests.auth import _basic_auth_str
import pytest

def test_basic_auth_str_non_latin1_raises():
    username = "user\u2603"  # Snowman, not latin1
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)
