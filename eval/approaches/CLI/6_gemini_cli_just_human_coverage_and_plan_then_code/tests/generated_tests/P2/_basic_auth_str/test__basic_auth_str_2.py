import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1():
    # Scenario: Username with Latin1 character (ñ is \xf1 in latin1)
    # userñ:pass -> user\xf1:pass
    # user\xf1:pass base64 -> dXNlcnH6cGFzcw== (Wait, let's verify logic)
    # "userñ" (utf8) -> encode('latin1') -> b'user\xf1'
    # b":".join(...) -> b'user\xf1:pass'
    # b64encode -> b'dXNlcvE6cGFzcw=='
    
    # We test that it doesn't raise error and produces a string starting with Basic
    result = _basic_auth_str("userñ", "pass")
    assert result.startswith("Basic ")
    # Decoding checks:
    token = result.split(" ")[1]
    import base64
    decoded = base64.b64decode(token).decode('latin1')
    assert decoded == "userñ:pass"
