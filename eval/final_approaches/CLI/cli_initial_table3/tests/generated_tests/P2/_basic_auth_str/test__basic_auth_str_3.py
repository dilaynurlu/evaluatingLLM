import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_latin1_characters():
    """
    Test _basic_auth_str with latin1 characters which are allowed in headers.
    """
    username = "user\u00e9"  # useré
    password = "pass\u00f1"  # passñ
    
    # "useré:passñ" encoded in latin1 then base64
    # "user\xe9:pass\xf1"
    # b"user\xe9:pass\xf1" -> b64encode -> b'dXNlcmt2cGFzc/E='
    # Wait, lets double check base64 of b'user\xe9:pass\xf1'
    # b'user\xe9:pass\xf1' is b'\x75\x73\x65\x72\xe9\x3a\x70\x61\x73\x73\xf1'
    # b64: dXNlcmt2cGFzc/E= (Wait, my mental calc might be off, I'll rely on the function logic and assert correctness by decoding)
    
    result = _basic_auth_str(username, password)
    
    # We can verify by decoding the result
    import base64
    prefix = "Basic "
    assert result.startswith(prefix)
    encoded = result[len(prefix):]
    decoded = base64.b64decode(encoded).decode("latin1")
    
    assert decoded == f"{username}:{password}"
