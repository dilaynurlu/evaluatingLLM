import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_with_latin1_chars():
    """
    Test _basic_auth_str with strings containing Latin-1 characters.
    Verifies that the input strings are correctly encoded as latin1 before base64 encoding.
    """
    # 'ñ' is \u00f1 (valid in latin1), 'å' is \u00e5 (valid in latin1)
    username = "user\u00f1ame" 
    password = "p\u00e5ssword"
    
    u_latin1 = username.encode("latin1")
    p_latin1 = password.encode("latin1")
    
    raw_joined = u_latin1 + b":" + p_latin1
    b64_val = base64.b64encode(raw_joined).decode("ascii")
    expected = "Basic " + b64_val
    
    result = _basic_auth_str(username, password)
    
    assert result == expected