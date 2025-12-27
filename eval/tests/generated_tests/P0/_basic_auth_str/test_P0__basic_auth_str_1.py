import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_simple_strings():
    """
    Test _basic_auth_str with standard ASCII strings.
    Verifies that the function correctly concatenates username and password
    with a colon, encodes them using base64, and prepends 'Basic '.
    """
    username = "Aladdin"
    password = "open sesame"
    
    # Expected logic: "Aladdin:open sesame" -> base64 encoded
    # b"Aladdin:open sesame" base64 is b"QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    expected_token = "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    expected = "Basic " + expected_token
    
    result = _basic_auth_str(username, password)
    
    assert result == expected