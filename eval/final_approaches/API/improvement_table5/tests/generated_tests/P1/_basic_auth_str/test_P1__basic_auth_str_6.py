import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed string and bytes arguments.
    Verifies that the function handles a combination where one argument needs encoding
    and the other is already bytes.
    """
    username = "user"    # str, needs latin1 encoding
    password = b"pass"   # bytes, used as is
    
    expected_user = username.encode("latin1")
    expected_pass = password # already bytes
    raw_credentials = expected_user + b":" + expected_pass
    encoded_credentials = base64.b64encode(raw_credentials).decode("ascii")
    expected_auth_str = f"Basic {encoded_credentials}"
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str