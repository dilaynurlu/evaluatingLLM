import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_strings():
    # 'ñ' is \xf1 in latin1
    # 'å' is \xe5 in latin1
    username = "niño"
    password = "pås"
    
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    
    raw_token = u_bytes + b":" + p_bytes
    
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    assert _basic_auth_str(username, password) == expected