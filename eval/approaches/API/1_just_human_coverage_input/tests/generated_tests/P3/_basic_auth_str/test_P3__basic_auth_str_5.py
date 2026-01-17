import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_warning_int_username():
    username = 12345
    password = "test_secret"
    
    # Golden Master Calculation:
    # "12345:test_secret"
    # Base64: MTIzNDU6dGVzdF9zZWNyZXQ=
    expected = "Basic MTIzNDU6dGVzdF9zZWNyZXQ="
    
    # Use pytest.warns for cleaner assertion of warnings compared to raw context managers
    with pytest.warns(DeprecationWarning, match="Non-string usernames"):
        result = _basic_auth_str(username, password)
    
    assert result == expected