import pytest
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_normal_strings():
    username = "Aladdin"
    password = "open sesame"
    expected_encoded = base64.b64encode(b"Aladdin:open sesame").decode("ascii")
    expected = "Basic " + expected_encoded
    
    assert _basic_auth_str(username, password) == expected
