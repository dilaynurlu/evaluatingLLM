import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_strings():
    username = ""
    password = ""
    
    # Empty strings encode to empty bytes
    u_bytes = b""
    p_bytes = b""
    
    raw_token = u_bytes + b":" + p_bytes  # Result is b":"
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    assert _basic_auth_str(username, password) == expected