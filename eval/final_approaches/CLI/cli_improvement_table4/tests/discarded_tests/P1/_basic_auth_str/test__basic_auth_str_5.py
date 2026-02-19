import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_unicode_error():
    """Test _basic_auth_str raises UnicodeEncodeError for non-Latin-1 chars."""
    username = "user😊"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)
