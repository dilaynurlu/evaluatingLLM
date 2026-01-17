import pytest
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_password_with_colon():
    username = "user"
    password = "pass:word"
    # "user" + ":" + "pass:word" -> "user:pass:word"
    expected_encoded = base64.b64encode(b"user:pass:word").decode("ascii")
    expected = "Basic " + expected_encoded
    
    assert _basic_auth_str(username, password) == expected
