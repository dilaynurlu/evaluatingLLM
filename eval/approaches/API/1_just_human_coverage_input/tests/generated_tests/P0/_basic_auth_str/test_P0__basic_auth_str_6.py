import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_strings():
    """
    Test _basic_auth_str with empty username and password.
    Verifies correct handling of empty strings resulting in a base64 encoded colon.
    """
    username = ""
    password = ""
    
    # Joined string is just ":"
    raw_joined = b":"
    b64_val = base64.b64encode(raw_joined).decode("ascii")
    expected = "Basic " + b64_val
    
    result = _basic_auth_str(username, password)
    
    assert result == expected