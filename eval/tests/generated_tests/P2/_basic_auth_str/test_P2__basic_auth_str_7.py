import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_bytes_and_string():
    username = "user"
    password = b"pass"
    
    # Logic: username (str) -> latin1 encoded bytes
    #        password (bytes) -> stays bytes
    u_bytes = username.encode("latin1")
    p_bytes = password
    
    raw_token = u_bytes + b":" + p_bytes
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    assert _basic_auth_str(username, password) == expected