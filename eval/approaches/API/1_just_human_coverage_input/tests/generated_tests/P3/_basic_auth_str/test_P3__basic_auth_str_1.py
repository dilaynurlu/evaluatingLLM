from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii_credentials():
    # Use standard placeholder credentials instead of "Aladdin"/"open sesame" 
    # to avoid confusion with secrets, though RFC 7617 uses Aladdin as an example.
    # Here we stick to the RFC example for Golden Master verification but ensure 
    # the variables are named safely.
    username = "Aladdin"
    password = "open sesame"
    
    # Golden Master: 
    # "Aladdin:open sesame" -> base64 -> "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    # Expected result must be prefixed with "Basic "
    expected = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    result = _basic_auth_str(username, password)
    assert result == expected