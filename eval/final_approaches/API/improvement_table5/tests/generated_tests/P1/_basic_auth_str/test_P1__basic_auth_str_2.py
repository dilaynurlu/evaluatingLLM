import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_inputs():
    """
    Test _basic_auth_str with bytes arguments.
    Verifies that bytes are used directly (bypassing latin1 encoding step for strings),
    joined, and correctly base64 encoded.
    """
    username = b"Aladdin"
    password = b"open sesame"
    
    # When inputs are bytes, they are joined directly
    raw_credentials = username + b":" + password
    encoded_credentials = base64.b64encode(raw_credentials).decode("ascii")
    expected_auth_str = f"Basic {encoded_credentials}"
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str