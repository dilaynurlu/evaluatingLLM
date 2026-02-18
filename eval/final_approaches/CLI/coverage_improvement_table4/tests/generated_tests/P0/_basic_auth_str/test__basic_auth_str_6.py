from requests.auth import _basic_auth_str
from base64 import b64decode

def test_basic_auth_str_6():
    # Test empty username and password
    auth = _basic_auth_str("", "")
    # : -> Og==
    assert auth == "Basic Og=="
