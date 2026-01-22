import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_with_colons():
    # Colons in username or password are valid characters for the inputs
    username = "user:name"
    password = "pass:word"
    
    raw_creds = (username + ":" + password).encode("latin1")
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert _basic_auth_str(username, password) == expected