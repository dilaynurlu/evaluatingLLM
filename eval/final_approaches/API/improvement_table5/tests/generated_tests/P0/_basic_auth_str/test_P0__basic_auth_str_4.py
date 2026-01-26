import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test mixed inputs: String username and Bytes password.
    Verifies that the function handles mixed types correctly by encoding the string
    and leaving the bytes as-is.
    """
    username = "stringuser"
    password = b"bytespassword"
    
    # Username (str) -> encode latin1
    # Password (bytes) -> as is
    joined = username.encode("latin1") + b":" + password
    
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    result = _basic_auth_str(username, password)
    assert result == expected