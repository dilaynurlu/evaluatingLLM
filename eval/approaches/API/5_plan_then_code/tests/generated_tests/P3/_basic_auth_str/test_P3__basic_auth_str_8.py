import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_encode_error_check():
    """
    Test _basic_auth_str with characters invalid in Latin-1.
    Confirms strict Latin-1 enforcement raises UnicodeEncodeError.
    This test verifies that the library currently refuses characters not representable
    in ISO-8859-1, rather than falling back to UTF-8 silently.
    """
    # The snowman character \u2603 is not representable in latin1
    username = "snowman\u2603"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError) as excinfo:
        _basic_auth_str(username, password)
    
    assert "latin-1" in str(excinfo.value)