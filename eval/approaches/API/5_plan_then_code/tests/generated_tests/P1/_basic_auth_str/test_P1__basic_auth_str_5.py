import base64
import pytest
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_password_type():
    # Passing an integer triggers a DeprecationWarning and conversion to string
    username = "my_username"
    password = 67890
    
    expected_bytes = username.encode("latin1") + b":" + str(password).encode("latin1")
    expected_b64 = base64.b64encode(expected_bytes).decode("ascii")
    expected_str = "Basic " + expected_b64
    
    with pytest.warns(DeprecationWarning, match="Non-string passwords"):
        result = _basic_auth_str(username, password)
        
    assert result == expected_str