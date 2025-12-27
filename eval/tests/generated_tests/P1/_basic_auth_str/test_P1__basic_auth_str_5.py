import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_string_and_bytes():
    """
    Test _basic_auth_str with a mix of string and bytes inputs.
    Verifies that the string input is encoded to latin1 and joined correctly with the bytes input.
    """
    username = "string_user"
    password = b"bytes_pass"
    
    # Logic:
    # username (str) -> encoded to latin1 bytes
    # password (bytes) -> remains bytes
    u_bytes = username.encode("latin1")
    
    combined = u_bytes + b":" + password
    encoded_part = base64.b64encode(combined).decode("utf-8")
    expected_auth_str = f"Basic {encoded_part}"
    
    assert _basic_auth_str(username, password) == expected_auth_str