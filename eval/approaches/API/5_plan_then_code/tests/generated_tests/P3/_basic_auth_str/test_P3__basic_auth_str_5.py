import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_int_username_verification():
    """
    Test _basic_auth_str with a non-string (int) username.
    Refined to verify the deprecation warning and that the integer is 
    correctly converted to a string in the output.
    """
    username = 123456
    password = "password"
    
    with pytest.warns(DeprecationWarning, match="Non-string usernames"):
        result = _basic_auth_str(username, password)
    
    assert result.startswith("Basic ")
    token = result.split(" ")[1]
    decoded_str = base64.b64decode(token).decode("latin1")
    
    # Verify strict equality of the converted content
    assert decoded_str == f"{str(username)}:{password}"