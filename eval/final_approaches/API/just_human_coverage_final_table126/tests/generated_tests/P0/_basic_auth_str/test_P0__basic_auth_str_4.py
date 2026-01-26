import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    # Test with one str and one bytes
    username = "user"
    password = b"pass"
    
    # Logic: str input is encoded to latin1, bytes input remains as is
    raw_creds = username.encode("latin1") + b":" + password
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert _basic_auth_str(username, password) == expected