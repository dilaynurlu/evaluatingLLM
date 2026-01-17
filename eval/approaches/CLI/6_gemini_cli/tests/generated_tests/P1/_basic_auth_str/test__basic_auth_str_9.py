import pytest
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_mixed_bytes_and_str():
    username = b"user"
    password = "password"
    expected_encoded = base64.b64encode(b"user:password").decode("ascii")
    expected = "Basic " + expected_encoded
    
    assert _basic_auth_str(username, password) == expected
