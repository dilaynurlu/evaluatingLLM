import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes():
    """
    Test _basic_auth_str with bytes inputs.
    Verifies that bytes are used directly without re-encoding to latin1.
    """
    username = b"user"
    password = b"pass"

    # Expected calculation:
    # 1. Inputs are bytes, so no encoding step
    # 2. Joined with colon
    raw_creds = username + b":" + password
    # 3. Base64 encoded
    expected_b64 = base64.b64encode(raw_creds).decode("ascii")
    expected_auth = "Basic " + expected_b64

    result = _basic_auth_str(username, password)
    
    assert result == expected_auth