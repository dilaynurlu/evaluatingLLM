import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed string username and bytes password.
    Verifies correct concatenation of encoded string and raw bytes.
    """
    test_user = "string_user"
    test_pass = b"bytes_pass"
    
    result = _basic_auth_str(test_user, test_pass)
    
    assert result.startswith("Basic ")
    token = result.split(" ", 1)[1]
    
    decoded_bytes = base64.b64decode(token)
    
    # Expected behavior:
    # 1. Username (str) is encoded to latin1 bytes
    # 2. Password (bytes) is used as-is
    # 3. Joined by b':'
    expected_content = test_user.encode("latin1") + b":" + test_pass
    
    assert decoded_bytes == expected_content