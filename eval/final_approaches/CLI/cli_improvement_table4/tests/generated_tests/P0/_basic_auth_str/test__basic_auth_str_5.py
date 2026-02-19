from requests.auth import _basic_auth_str
from base64 import b64decode

def test_basic_auth_str_5():
    # Test username with colon
    username = "user:name"
    password = "password"
    auth = _basic_auth_str(username, password)
    # user:name:password
    decoded = b64decode(auth.split(" ")[1]).decode('latin1')
    assert decoded == "user:name:password"
