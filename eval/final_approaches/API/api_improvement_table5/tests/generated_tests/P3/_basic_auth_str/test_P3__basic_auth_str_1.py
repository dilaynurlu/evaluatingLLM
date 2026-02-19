from requests.auth import _basic_auth_str

def test_basic_auth_str_simple_ascii():
    """
    Test _basic_auth_str with simple ASCII strings for username and password.
    
    This verifies the standard happy path using the RFC 7617 example.
    We use a hardcoded Known Answer Test (KAT) to ensure the implementation
    conforms to the standard rather than replicating the implementation logic.
    """
    username = "Aladdin"
    password = "open sesame"
    
    # RFC 7617 example: "Aladdin:open sesame" -> "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    expected = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    result = _basic_auth_str(username, password)
    
    assert result == expected
    assert isinstance(result, str)