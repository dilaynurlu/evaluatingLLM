import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_error():
    """
    Test string input containing characters that cannot be encoded in Latin-1.
    Should raise UnicodeEncodeError.
    """
    # \u2603 is a unicode snowman, invalid in latin1
    username = "snowman\u2603"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)