import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_error():
    username = "user\u1234" # Ethiopic syllable, not in latin1
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)
