import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_raises_unicode_encode_error():
    # Test characters outside Latin-1 range
    # \u2603 is SNOWMAN, which cannot be encoded in latin1
    username = "user\u2603"
    password = "password"
    
    # The function attempts .encode('latin1') on string inputs,
    # which should raise UnicodeEncodeError for non-latin1 chars.
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)