import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_string_and_bytes():
    username = "Aladdin"
    password = b"open sesame"
    
    # Expected construction logic:
    # 1. String username is encoded to latin1
    # 2. Bytes password is used as-is
    # 3. Joined with colon
    user_bytes = username.encode('latin1')
    pass_bytes = password
    raw = b':'.join((user_bytes, pass_bytes))
    
    encoded = base64.b64encode(raw).strip().decode('ascii')
    expected = "Basic " + encoded
    
    assert _basic_auth_str(username, password) == expected