import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii():
    username = "Aladdin"
    password = "open sesame"
    
    # Expected behavior: encode str to latin1, join with colon, b64 encode, prepend Basic
    raw_creds = (username + ":" + password).encode("latin1")
    b64_creds = base64.b64encode(raw_creds).decode("utf-8")
    expected = "Basic " + b64_creds
    
    assert _basic_auth_str(username, password) == expected