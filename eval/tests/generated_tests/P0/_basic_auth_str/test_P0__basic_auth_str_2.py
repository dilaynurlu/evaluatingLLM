from requests.auth import _basic_auth_str

def test_basic_auth_str_with_bytes():
    """
    Test _basic_auth_str with bytes input.
    Verifies that bytes inputs are handled directly without encoding conversion,
    avoiding the DeprecationWarning for non-strings (since bytes are allowed implicitly 
    via basestring compat or direct handling in some versions, but mainly ensuring 
    they are joined and encoded correctly).
    """
    username = b"Aladdin"
    password = b"open sesame"
    
    # b"Aladdin" + b":" + b"open sesame" -> b"Aladdin:open sesame"
    # Base64 of b"Aladdin:open sesame" -> b"QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    expected = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    result = _basic_auth_str(username, password)
    
    assert result == expected