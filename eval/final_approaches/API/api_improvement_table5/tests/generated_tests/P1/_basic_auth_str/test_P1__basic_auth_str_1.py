import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_simple_strings():
    """
    Test _basic_auth_str with standard string arguments.
    Verifies that strings are encoded to latin1, joined with a colon, 
    and returned as a valid Basic Auth base64 string.
    """
    username = "Aladdin"
    password = "open sesame"
    
    # Expected construction logic based on function contract:
    # 1. Encode parts to latin1
    # 2. Join with colon
    # 3. Base64 encode
    # 4. Prepend "Basic "
    
    user_bytes = username.encode("latin1")
    pass_bytes = password.encode("latin1")
    raw_credentials = user_bytes + b":" + pass_bytes
    encoded_credentials = base64.b64encode(raw_credentials).decode("ascii")
    expected_auth_str = f"Basic {encoded_credentials}"
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str