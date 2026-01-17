
import pytest
from requests.auth import _basic_auth_str
from base64 import b64decode

def test__basic_auth_str_simple():
    username = "user"
    password = "password"
    auth_str = _basic_auth_str(username, password)
    assert auth_str.startswith("Basic ")
    decoded = b64decode(auth_str.split(" ")[1]).decode("latin1")
    assert decoded == "user:password"
