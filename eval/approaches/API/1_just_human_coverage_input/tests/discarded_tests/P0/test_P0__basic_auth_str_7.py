import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_encode_error():
    """
    Test _basic_auth_str with a username containing characters not representable in Latin-1.
    Verifies that UnicodeEncodeError is raised, confirming the enforcement of Latin-1 encoding for strings.
    """
    # \u2603 is the SNOWMAN character, which cannot be encoded in latin1
    username = "user\u2603"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)