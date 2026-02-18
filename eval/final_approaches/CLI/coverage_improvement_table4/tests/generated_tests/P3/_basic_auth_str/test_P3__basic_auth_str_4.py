import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_encoding():
    # characters that are valid in latin1 but not ascii
    username = "user\u00E9" # useré
    password = "pass\u00F1" # passñ
    
    # "user\xe9:pass\xf1" -> b"user\xe9:pass\xf1" (latin1)
    # b64encode(b"user\xe9:pass\xf1")
    # Python: base64.b64encode('user\u00e9:pass\u00f1'.encode('latin1')) -> b'dXNlcuk6cGFzc/E='
    expected = "Basic dXNlcuk6cGFzc/E="
    assert _basic_auth_str(username, password) == expected
