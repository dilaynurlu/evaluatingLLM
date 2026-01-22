import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii_strings():
    username = "Aladdin"
    password = "open sesame"
    
    # Calculate expected value manually
    # 1. Strings are encoded to latin1 (ascii is a subset)
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    
    # 2. Joined with colon
    raw_token = u_bytes + b":" + p_bytes
    
    # 3. Base64 encoded and decoded to native string
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    assert _basic_auth_str(username, password) == expected