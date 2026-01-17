import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_input_with_control_chars():
    """
    Test _basic_auth_str with bytes inputs.
    Refined to verify by decoding and checking that control characters
    (null bytes, newlines) are preserved in the payload.
    """
    # Using control characters to ensure they are treated as raw bytes
    username = b"user\0name"
    password = b"pass\nword"
    
    result = _basic_auth_str(username, password)
    
    assert result.startswith("Basic ")
    token = result.split(" ")[1]
    
    # Decode and verify exact byte match
    decoded_bytes = base64.b64decode(token)
    expected_payload = username + b":" + password
    
    assert decoded_bytes == expected_payload