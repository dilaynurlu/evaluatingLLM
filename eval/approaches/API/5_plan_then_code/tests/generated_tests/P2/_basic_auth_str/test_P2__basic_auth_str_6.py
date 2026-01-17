import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_chars():
    """
    Test _basic_auth_str with string inputs containing Latin-1 characters (non-ASCII).
    Verifies that characters valid in Latin-1 but outside ASCII are encoded correctly.
    """
    # 'ñ' is \xf1 in latin1
    username = "señor"
    password = "123"

    user_bytes = username.encode("latin1")
    pass_bytes = password.encode("latin1")
    
    raw_creds = user_bytes + b":" + pass_bytes
    expected_b64 = base64.b64encode(raw_creds).decode("ascii")
    expected_auth = "Basic " + expected_b64

    result = _basic_auth_str(username, password)
    
    assert result == expected_auth