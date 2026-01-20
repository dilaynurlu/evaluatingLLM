import pytest
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_latin1_special_chars():
    username = "user\u00f1" # userñ
    password = "password"
    # u00f1 is valid in latin1
    expected_encoded = base64.b64encode(b"user\xf1:password").decode("ascii")
    expected = "Basic " + expected_encoded
    
    assert _basic_auth_str(username, password) == expected
