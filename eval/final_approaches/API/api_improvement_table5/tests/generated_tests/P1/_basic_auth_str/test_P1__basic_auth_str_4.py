import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_characters():
    """
    Test _basic_auth_str with strings containing extended latin1 characters.
    Verifies that characters within the latin1 range (but outside ASCII) 
    are encoded correctly without error.
    """
    # 'ñ' is \xf1 in latin1
    username = "user\xf1" 
    # 'ü' is \xfc in latin1
    password = "pass\xfc"
    
    expected_user = username.encode("latin1")
    expected_pass = password.encode("latin1")
    raw_credentials = expected_user + b":" + expected_pass
    encoded_credentials = base64.b64encode(raw_credentials).decode("ascii")
    expected_auth_str = f"Basic {encoded_credentials}"
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str