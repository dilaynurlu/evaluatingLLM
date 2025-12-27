import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_standard_ascii():
    """
    Test _basic_auth_str with standard ASCII string inputs.
    Verifies the Basic Auth header generation for typical username and password.
    """
    username = "Aladdin"
    password = "open sesame"
    
    # Expected construction: "Basic " + base64("Aladdin:open sesame")
    # "Aladdin:open sesame" -> b"QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    expected_auth_str = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    result = _basic_auth_str(username, password)
    
    assert result == expected_auth_str
    assert isinstance(result, str)