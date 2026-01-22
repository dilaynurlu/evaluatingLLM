import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_inputs():
    """
    Test _basic_auth_str with bytes inputs.
    Verifies that bytes are used directly without latin1 encoding step.
    """
    username = b"user"
    password = b"pass"
    
    result = _basic_auth_str(username, password)
    
    # When inputs are bytes, they are joined directly
    raw_payload = b":".join((username, password))
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected