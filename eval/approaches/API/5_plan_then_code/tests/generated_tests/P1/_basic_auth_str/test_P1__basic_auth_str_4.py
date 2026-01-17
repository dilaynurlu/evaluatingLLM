import base64
import pytest
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_username_type():
    # Passing an integer triggers a DeprecationWarning and conversion to string
    username = 12345
    password = "my_password"
    
    expected_bytes = str(username).encode("latin1") + b":" + password.encode("latin1")
    expected_b64 = base64.b64encode(expected_bytes).decode("ascii")
    expected_str = "Basic " + expected_b64
    
    with pytest.warns(DeprecationWarning, match="Non-string usernames"):
        result = _basic_auth_str(username, password)
        
    assert result == expected_str