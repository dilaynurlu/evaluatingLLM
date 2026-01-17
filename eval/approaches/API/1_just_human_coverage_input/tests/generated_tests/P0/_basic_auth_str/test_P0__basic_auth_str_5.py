import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_warning():
    """
    Test _basic_auth_str with non-string (int) username.
    Verifies that a DeprecationWarning is issued and the integer is converted to a string.
    """
    username = 12345
    password = "password"
    
    # Expect a DeprecationWarning because username is an int
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(username, password)
        
    # Expected behavior: int is converted to string, then handled as a string
    u_str = str(username)
    u_bytes = u_str.encode("latin1")
    p_bytes = password.encode("latin1")
    
    raw_joined = u_bytes + b":" + p_bytes
    b64_val = base64.b64encode(raw_joined).decode("ascii")
    expected = "Basic " + b64_val
    
    assert result == expected