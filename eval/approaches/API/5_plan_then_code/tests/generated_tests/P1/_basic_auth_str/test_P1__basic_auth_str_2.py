import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_chars():
    # Testing with Latin-1 supported characters
    username = "user\u00e9"  # 'useré'
    password = "p\u00f1wd"    # 'pñwd'
    
    expected_bytes = username.encode("latin1") + b":" + password.encode("latin1")
    expected_b64 = base64.b64encode(expected_bytes).decode("ascii")
    expected_str = "Basic " + expected_b64
    
    assert _basic_auth_str(username, password) == expected_str