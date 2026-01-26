import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_strings():
    """
    Test empty strings for username and password.
    Should result in base64 encoding of a single colon.
    """
    username = ""
    password = ""
    
    joined = b":"
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    result = _basic_auth_str(username, password)
    assert result == expected