import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_input():
    # Bytes inputs are used directly without latin1 encoding step
    username = b"user_bytes"
    password = b"pass_bytes"
    
    expected_bytes = username + b":" + password
    expected_b64 = base64.b64encode(expected_bytes).decode("ascii")
    expected_str = "Basic " + expected_b64
    
    assert _basic_auth_str(username, password) == expected_str