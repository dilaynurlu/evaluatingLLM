import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_valid_chars():
    """
    Test _basic_auth_str with strings containing Latin-1 characters (e.g., £).
    Verifies that the function encodes strings to latin1 bytes before base64 encoding.
    """
    username = "user"
    password = "p\u00a3ss"  # p£ss, \u00a3 is valid in latin-1
    
    # Logic:
    # 1. Strings encoded to latin1: "user" -> b"user", "p\u00a3ss" -> b"p\xa3ss"
    # 2. Joined: b"user:p\xa3ss"
    # 3. Base64 encoded
    
    raw_bytes = username.encode('latin1') + b':' + password.encode('latin1')
    expected_b64 = base64.b64encode(raw_bytes).decode('ascii')
    expected = "Basic " + expected_b64
    
    result = _basic_auth_str(username, password)
    
    assert result == expected