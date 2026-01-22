import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_encode_error():
    """
    Test _basic_auth_str with characters outside the Latin-1 range.
    Should raise UnicodeEncodeError.
    """
    # Latin-1 supports up to \u00ff.
    # \u0100 is the first character outside Latin-1 (Amacron).
    username = "user\u0100"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)

    # The Euro sign \u20ac is also a common failure case for latin1
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str("user\u20ac", "password")