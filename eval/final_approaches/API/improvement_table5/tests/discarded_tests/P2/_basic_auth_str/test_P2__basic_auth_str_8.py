import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_error():
    """
    Test _basic_auth_str with characters not representable in Latin-1.
    Since the function forces 'latin1' encoding for strings, this should raise UnicodeEncodeError.
    """
    # U+2603 is the Snowman character, which is not in ISO-8859-1.
    username = "snowman\u2603"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)