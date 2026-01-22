import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_inputs():
    """
    Test _basic_auth_str with a mix of string and bytes inputs.
    Verifies the handling where strings are encoded to latin1 and bytes remain as is.
    """
    username = "user"
    password = b"pass"
    
    result = _basic_auth_str(username, password)
    
    # Username is str -> encoded to latin1
    # Password is bytes -> kept as is
    # Joined by b':'
    username_bytes = username.encode("latin1")
    raw_payload = b":".join((username_bytes, password))
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected