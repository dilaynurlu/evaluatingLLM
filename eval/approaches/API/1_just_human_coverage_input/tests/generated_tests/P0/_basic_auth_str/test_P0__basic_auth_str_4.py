import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_input():
    """
    Test _basic_auth_str with mixed string and bytes input.
    Verifies that the string input is encoded to latin1 while the bytes input is used as-is.
    """
    username = "user"
    password = b"pass"
    
    # Username is str, so it gets encoded to latin1
    u_bytes = username.encode("latin1")
    # Password is bytes, so it is used directly
    p_bytes = password
    
    raw_joined = u_bytes + b":" + p_bytes
    b64_val = base64.b64encode(raw_joined).decode("ascii")
    expected = "Basic " + b64_val
    
    result = _basic_auth_str(username, password)
    
    assert result == expected