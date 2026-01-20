
import pytest
from requests.auth import _basic_auth_str
from base64 import b64decode

def test__basic_auth_str_mixed_str_bytes():
    username = "user"
    password = b"password"
    auth_str = _basic_auth_str(username, password)
    decoded = b64decode(auth_str.split(" ")[1]).decode("latin1")
    assert decoded == "user:password"
