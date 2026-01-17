import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_input():
    """
    Test _basic_auth_str with bytes input.
    Verifies that bytes inputs bypass the latin1 encoding step and are joined directly.
    """
    username = b"user"
    password = b"pass"
    
    # When inputs are bytes, no encoding conversion happens
    raw_joined = username + b":" + password
    b64_val = base64.b64encode(raw_joined).decode("ascii")
    expected = "Basic " + b64_val
    
    result = _basic_auth_str(username, password)
    
    assert result == expected