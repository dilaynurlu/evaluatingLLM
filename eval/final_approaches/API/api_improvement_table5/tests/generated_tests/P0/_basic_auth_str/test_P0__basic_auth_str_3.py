import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_input():
    """
    Test bytes inputs for username and password.
    Verifies that bytes inputs skip the latin1 encoding step and are joined directly.
    """
    username = b"userbytes"
    password = b"passbytes"
    
    # Bytes are joined directly without additional encoding
    joined = username + b":" + password
    
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    result = _basic_auth_str(username, password)
    assert result == expected