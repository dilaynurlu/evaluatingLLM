import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii_strings():
    """
    Test _basic_auth_str with simple ASCII strings.
    Verifies that strings are joined by a colon, encoded, and prefixed with 'Basic '.
    """
    username = "user"
    password = "password"
    
    result = _basic_auth_str(username, password)
    
    # Expected construction based on implementation details:
    # 1. Strings are encoded to latin1
    # 2. Joined by b':'
    # 3. Base64 encoded
    # 4. Decoded to native string (ascii/utf-8) and prefixed
    raw_payload = (username + ":" + password).encode("latin1")
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected