import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_inputs():
    username = b"user"
    password = b"pass"
    
    # When inputs are bytes, no latin1 encoding happens
    raw_token = username + b":" + password
    
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    assert _basic_auth_str(username, password) == expected