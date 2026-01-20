
import pytest
from requests.auth import _basic_auth_str
from base64 import b64decode

def test__basic_auth_str_colon_in_user():
    username = "user:name"
    password = "password"
    auth_str = _basic_auth_str(username, password)
    decoded = b64decode(auth_str.split(" ")[1]).decode("latin1")
    assert decoded == "user:name:password"
