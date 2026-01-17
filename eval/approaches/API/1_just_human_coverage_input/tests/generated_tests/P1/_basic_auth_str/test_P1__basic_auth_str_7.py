import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_strings():
    username = ""
    password = ""
    
    # Empty strings result in empty bytes after encoding
    # Joining them with ':' results in b":"
    raw = b":"
    
    encoded = base64.b64encode(raw).strip().decode('ascii')
    expected = "Basic " + encoded
    
    assert _basic_auth_str(username, password) == expected