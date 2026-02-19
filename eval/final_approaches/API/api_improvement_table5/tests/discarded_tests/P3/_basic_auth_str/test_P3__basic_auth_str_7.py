import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_encode_error():
    """
    Test _basic_auth_str with a string containing characters outside Latin-1.
    
    Since the function explicitly encodes string inputs using 'latin1',
    providing a character like a smiley (which is not in Latin-1) should
    raise a UnicodeEncodeError.
    """
    username = "user_😊"
    password = "secret_password"
    
    # "😊" (U+1F60A) cannot be encoded in latin1.
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)