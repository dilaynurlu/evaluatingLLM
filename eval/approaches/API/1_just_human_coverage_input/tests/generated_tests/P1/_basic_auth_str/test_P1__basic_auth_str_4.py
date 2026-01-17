import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_extended_chars():
    # Test characters within Latin-1 range but outside ASCII
    # \u00fc is 'ü' (Latin Small Letter U with Diaeresis)
    # \u00f6 is 'ö' (Latin Small Letter O with Diaeresis)
    username = "user\u00fc"
    password = "pass\u00f6"
    
    user_bytes = username.encode('latin1')
    pass_bytes = password.encode('latin1')
    raw = b':'.join((user_bytes, pass_bytes))
    
    encoded = base64.b64encode(raw).strip().decode('ascii')
    expected = "Basic " + encoded
    
    assert _basic_auth_str(username, password) == expected