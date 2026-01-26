import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii_strings():
    """
    Test _basic_auth_str with standard ASCII strings using known RFC 7617 vectors.
    Also verifies handling of special characters like colons and newlines within inputs.
    """
    # 1. Standard RFC 7617 example
    # 'Aladdin' : 'open sesame' -> 'Aladdin:open sesame'
    # Base64('Aladdin:open sesame') -> 'QWxhZGRpbjpvcGVuIHNlc2FtZQ=='
    username = "Aladdin"
    password = "open sesame"
    expected_auth_str = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, "Expected no warnings for valid ASCII strings"
    assert result == expected_auth_str

    # 2. Username containing a colon (Edge Case)
    # RFC 7617 allows this in encoding, though servers might parse it incorrectly.
    # 'User:Name' : 'Pass' -> 'User:Name:Pass'
    # Base64('User:Name:Pass') -> 'VXNlcjpOYW1lOlBhc3M='
    u_colon = "User:Name"
    p_colon = "Pass"
    expected_colon = "Basic VXNlcjpOYW1lOlBhc3M="
    assert _basic_auth_str(u_colon, p_colon) == expected_colon

    # 3. Inputs containing newlines (CRLF Injection checks)
    # The function should blindly encode these, preventing HTTP splitting 
    # if the output is used as a header value, but the encoded string will contain the newline data.
    # 'User\n' : 'Pass' -> 'User\n:Pass'
    # Base64('User\n:Pass') -> 'VXNlcgo6UGFzcw=='
    u_newline = "User\n"
    p_newline = "Pass"
    expected_newline = "Basic VXNlcgo6UGFzcw=="
    assert _basic_auth_str(u_newline, p_newline) == expected_newline