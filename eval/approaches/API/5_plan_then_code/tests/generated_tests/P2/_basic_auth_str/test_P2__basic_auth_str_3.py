import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed string and bytes inputs.
    Verifies that the function handles a combination of bytes and string arguments correctly.
    """
    username = b"myuser"
    password = "mypassword"

    # Expected calculation:
    # username is bytes -> kept as is
    # password is str -> encoded to latin1
    user_bytes = username
    pass_bytes = password.encode("latin1")
    
    raw_creds = user_bytes + b":" + pass_bytes
    expected_b64 = base64.b64encode(raw_creds).decode("ascii")
    expected_auth = "Basic " + expected_b64

    result = _basic_auth_str(username, password)
    
    assert result == expected_auth