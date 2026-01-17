import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii_credentials():
    username = "Aladdin"
    password = "open sesame"
    
    # Expected construction logic:
    # 1. Strings are encoded to latin1 bytes
    # 2. Joined with colon
    # 3. Base64 encoded
    # 4. Prefixed with "Basic "
    user_bytes = username.encode('latin1')
    pass_bytes = password.encode('latin1')
    raw = b':'.join((user_bytes, pass_bytes))
    
    # Note: Using standard base64 logic to verify implementation output
    encoded = base64.b64encode(raw).strip().decode('ascii')
    expected = "Basic " + encoded
    
    assert _basic_auth_str(username, password) == expected