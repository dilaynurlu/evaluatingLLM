import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_explicit_bytes():
    """
    Test _basic_auth_str with explicit bytes input.
    """
    username = b"user"
    password = b"pass"
    
    result = _basic_auth_str(username, password)
    
    import base64
    prefix = "Basic "
    assert result.startswith(prefix)
    encoded = result[len(prefix):]
    decoded = base64.b64decode(encoded)
    
    assert decoded == b"user:pass"
