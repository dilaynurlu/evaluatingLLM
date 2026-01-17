import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_standard_ascii():
    username = "Aladdin"
    password = "open sesame"
    
    # Expected behavior:
    # 1. Strings encoded to latin1
    # 2. Joined with colon
    # 3. Base64 encoded
    # 4. Prepended with "Basic "
    
    expected_bytes = username.encode("latin1") + b":" + password.encode("latin1")
    expected_b64 = base64.b64encode(expected_bytes).decode("ascii")
    expected_str = "Basic " + expected_b64
    
    assert _basic_auth_str(username, password) == expected_str