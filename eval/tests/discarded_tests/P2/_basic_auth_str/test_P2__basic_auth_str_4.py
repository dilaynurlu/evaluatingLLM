import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_error_non_latin1():
    # '€' (Euro sign) is NOT present in ISO-8859-1 (latin1)
    # It usually requires cp1252 or utf-8.
    # The function forces latin1, so this must raise UnicodeEncodeError.
    username = "user€"
    password = "password"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)