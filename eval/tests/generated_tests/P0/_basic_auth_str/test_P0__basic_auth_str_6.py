import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_strings():
    username = ""
    password = ""
    
    # Should result in just a colon encoded
    raw_creds = b":"
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert _basic_auth_str(username, password) == expected