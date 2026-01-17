import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_inputs_verification():
    """
    Test _basic_auth_str with empty strings.
    Refined to verify outcome by decoding.
    """
    username = ""
    password = ""
    
    result = _basic_auth_str(username, password)
    
    assert result.startswith("Basic ")
    token = result.split(" ")[1]
    decoded_bytes = base64.b64decode(token)
    
    # Should result in a single colon
    assert decoded_bytes == b":"