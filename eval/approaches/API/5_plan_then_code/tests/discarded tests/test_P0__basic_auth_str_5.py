import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_error():
    """
    Test _basic_auth_str with characters not representable in Latin-1.
    Since the implementation explicitly encodes strings as 'latin1', this should raise UnicodeEncodeError.
    """
    # \u2603 is SNOWMAN, which is not in ISO-8859-1 (Latin-1)
    username = "user\u2603"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)