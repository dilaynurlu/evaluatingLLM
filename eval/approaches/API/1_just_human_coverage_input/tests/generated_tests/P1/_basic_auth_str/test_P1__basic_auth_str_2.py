import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_credentials():
    username = b"Aladdin"
    password = b"open sesame"
    
    # Expected construction logic for bytes:
    # 1. Bytes are used as-is (no encoding step)
    # 2. Joined with colon
    # 3. Base64 encoded
    # 4. Prefixed with "Basic "
    raw = b':'.join((username, password))
    
    encoded = base64.b64encode(raw).strip().decode('ascii')
    expected = "Basic " + encoded
    
    assert _basic_auth_str(username, password) == expected