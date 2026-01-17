import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_str_and_bytes_verification():
    """
    Test _basic_auth_str with mixed string and bytes inputs.
    Refined to verify outcome by decoding the result.
    """
    username = "user"
    password = b"secret_pass"
    
    result = _basic_auth_str(username, password)
    
    assert result.startswith("Basic ")
    token = result.split(" ")[1]
    decoded_bytes = base64.b64decode(token)
    
    # Username (str) is encoded to latin1, password (bytes) is concatenated as-is
    expected_payload = username.encode("latin1") + b":" + password
    
    assert decoded_bytes == expected_payload