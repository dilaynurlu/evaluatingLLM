import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_str_and_bytes():
    # Mixed input types: str is encoded, bytes is used as-is
    username = "string_user"
    password = b"bytes_pass"
    
    expected_bytes = username.encode("latin1") + b":" + password
    expected_b64 = base64.b64encode(expected_bytes).decode("ascii")
    expected_str = "Basic " + expected_b64
    
    assert _basic_auth_str(username, password) == expected_str