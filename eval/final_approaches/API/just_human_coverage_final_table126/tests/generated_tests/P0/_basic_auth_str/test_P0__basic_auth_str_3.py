import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes():
    # Test with bytes input, no latin1 encoding step should occur
    username = b"user"
    password = b"pass"
    
    raw_creds = username + b":" + password
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert _basic_auth_str(username, password) == expected