import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_inputs():
    """
    Test _basic_auth_str with bytes inputs.
    Verifies that bytes are used directly without re-encoding to latin1.
    """
    username = b"byteuser"
    password = b"bytepass"
    
    # When inputs are bytes, the function joins them directly.
    combined = username + b":" + password
    encoded_part = base64.b64encode(combined).decode("utf-8")
    expected_auth_str = f"Basic {encoded_part}"
    
    assert _basic_auth_str(username, password) == expected_auth_str