import pytest
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_username_with_colon():
    username = "user:name"
    password = "password"
    # "user:name" + ":" + "password" -> "user:name:password"
    expected_encoded = base64.b64encode(b"user:name:password").decode("ascii")
    expected = "Basic " + expected_encoded
    
    assert _basic_auth_str(username, password) == expected
