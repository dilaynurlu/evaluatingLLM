import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_simple_ascii():
    """
    Test standard ASCII string inputs for username and password.
    Should be encoded to latin1, joined, and base64 encoded.
    """
    username = "testuser"
    password = "testpassword"
    
    # Expected construction logic:
    # 1. Strings are encoded to latin1
    # 2. Joined by ':'
    # 3. Base64 encoded
    # 4. Prefixed with 'Basic '
    
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    joined = u_bytes + b":" + p_bytes
    
    # Standard base64.b64encode returns bytes without newlines for short inputs
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    result = _basic_auth_str(username, password)
    assert result == expected