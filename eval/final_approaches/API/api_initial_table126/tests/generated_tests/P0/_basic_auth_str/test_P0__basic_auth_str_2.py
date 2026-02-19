import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1():
    # Test with characters outside ASCII but valid in Latin-1
    username = "user\u00f1"  # 'ñ'
    password = "pass\u00fc"  # 'ü'
    
    raw_creds = (username + ":" + password).encode("latin1")
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert _basic_auth_str(username, password) == expected