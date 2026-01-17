
import pytest
from requests.auth import _basic_auth_str
from base64 import b64decode

def test__basic_auth_str_latin1_chars():
    username = "user£"
    password = "password"
    auth_str = _basic_auth_str(username, password)
    # The function encodes input as latin1 before b64 encoding
    # user£ -> user\xa3
    decoded_bytes = b64decode(auth_str.split(" ")[1])
    assert decoded_bytes == b"user\xa3:password"
